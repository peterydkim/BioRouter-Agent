/* BioRouter web client.
 *
 * All policy lives in the ruleset. This file renders it and never reasons past
 * it: no verdict is synthesised, no cell is inferred from a neighbour, and a
 * missing cell renders as missing rather than as permission.
 *
 * There is no network call after the initial data load and no storage of any
 * kind. A static page cannot receive the data it governs, which is the point.
 */
(function () {
  "use strict";

  var D = null;
  var VERDICT_CLASS = { 2: "v2", 1: "v1", 0: "v0" };

  /* Destination escalates the class. Origin is not the only input: a prompt
   * containing nothing sensitive still lands in gxp-record if the answer is
   * pasted into a submission module. */
  var DEST_CLASS = {
    "submission": "gxp-record",
    "gxp-record": "gxp-record",
    "safety-case": "pv",
    "patient-decision": "clin-id"
  };
  /* Which classes a piece of work can actually be reduced TO, and how.
   * Not every lower tier is reachable by de-identifying: gxp-record and pv are
   * set by destination and reporting obligation, so "de-identify down to
   * gxp-record" is not advice, it is a category error. Classes with no
   * reduction say so rather than inventing one. */
  var REDUCTION = {
    "clin-id": { to: ["clin-deid", "clin-anon"], how: "de-identify under HIPAA, or aggregate to a truly anonymous cut" },
    "clin-deid": { to: ["clin-anon"], how: "aggregate so that no individual record is recoverable" },
    "germline-seq": { to: ["clin-anon", "public"], how: "aggregate to allele counts or cohort frequencies where no individual genotype is recoverable — which aggregations qualify is the DPO's determination, not the requester's (open item 10)" },
    "ts-chem": { to: ["research-unpub", "internal"], how: "abstract away the differentiating structure or process detail" },
    "predec": { to: ["cci", "internal"], how: "strip the pre-decisional framing and the deal context" },
    "cci": { to: ["internal", "public"], how: "remove the commercially confidential specifics" },
    "research-unpub": { to: ["public"], how: "use published material only" },
    "pv": { to: [], how: null },
    "gxp-record": { to: [], how: null },
    "export-durc": { to: [], how: null }
  };
  var NO_REDUCTION_WHY = {
    "pv": "A pharmacovigilance case carries a reporting obligation, not just a confidentiality one. It does not de-identify into a lower class.",
    "gxp-record": "This class is set by where the output goes, not by what the input was. The only way out is for the output not to enter the record.",
    "export-durc": "Export control and DURC scope attach to the subject matter itself. De-identification does not reach them, and enclave containment does not cure a deemed export."
  };

  var DEST_LABEL = {
    "submission": "a regulatory submission",
    "gxp-record": "a GxP record or batch release",
    "safety-case": "a pharmacovigilance case",
    "patient-decision": "a decision about an identified patient"
  };

  function $(id) { return document.getElementById(id); }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function byId(list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }
  function platName(id) { var p = byId(D.platforms, id); return p ? (p.label || p.name || id) : id; }
  function platTier(id) { var p = byId(D.platforms, id); return p && p.tier ? p.tier : ""; }
  function className(id) { var c = byId(D.data_classes, id); return c ? c.label : id; }
  function classTier(id) { var c = byId(D.data_classes, id); return c ? c.tier : 0; }
  function ucName(id) { var u = byId(D.use_cases, id); return u ? u.label : id; }

  /* ── freshness ─────────────────────────────────────────────────────────── */
  function renderFreshness() {
    var reconciled = new Date(D.last_reconciled + "T00:00:00Z");
    var days = Math.floor((Date.now() - reconciled.getTime()) / 86400000);
    var stale = days > D.stale_after_days;
    var past = days > D.freshness_target_days;

    var box = $("freshness");
    box.className = "freshness" + (stale ? " stale" : "");
    box.appendChild(el("b", null, stale ? "Stale — distrust this answer"
      : past ? "Past reconciliation target" : "Unsigned draft"));

    var msg = "Reconciled " + days + " day" + (days === 1 ? "" : "s") + " ago against a "
      + D.freshness_target_days + "-day target. ";
    msg += "Ruleset " + D.ruleset_version + " is UNSIGNED: no security, privacy, QA or "
      + "legal reviewer has walked it. Treat every verdict as a starting hypothesis.";
    box.appendChild(document.createTextNode(msg));
  }

  /* ── selects ───────────────────────────────────────────────────────────── */
  function populate() {
    var w = $("work");
    D.use_cases.forEach(function (u) {
      w.appendChild(new Option(u.label, u.id));
    });
    var c = $("dclass");
    D.data_classes.forEach(function (k) {
      c.appendChild(new Option("Tier " + k.tier + " · " + k.id + " — " + k.label, k.id));
    });
    c.value = "research-unpub";
    var pl = $("plat");
    D.platforms.forEach(function (p) {
      pl.appendChild(new Option((p.label || p.name || p.id), p.id));
    });
  }

  function updateHints() {
    var cls = byId(D.data_classes, $("dclass").value);
    $("classHint").textContent = cls && cls.note ? cls.note : (cls ? cls.label : "");
    var uc = byId(D.use_cases, $("work").value);
    $("workHint").textContent = uc ? "Routing " + uc.label.toLowerCase() + "." : "";
  }

  /* ── the routing decision ──────────────────────────────────────────────── */
  function effectiveClass() {
    var chosen = $("dclass").value;
    var dest = $("dest").value;
    var destCls = DEST_CLASS[dest];
    if (destCls && classTier(destCls) > classTier(chosen)) {
      return { cls: destCls, escalatedFrom: chosen, dest: dest };
    }
    return { cls: chosen, escalatedFrom: null, dest: dest };
  }

  function rank(cls, work) {
    var rows = [];
    D.platforms.forEach(function (p) {
      var cell = D.matrix[p.id] ? D.matrix[p.id][cls] : null;
      if (!cell) { rows.push({ id: p.id, missing: true }); return; }
      var f = (D.fit[work] && D.fit[work][p.id]) || null;
      rows.push({
        id: p.id, verdict: cell.verdict, rule: cell.rule,
        approver: cell.approver || null,
        fit: f ? f.score : null, basis: f ? f.basis : null, note: f ? f.note : null
      });
    });
    rows.sort(function (a, b) {
      if (a.missing) return 1;
      if (b.missing) return -1;
      if (b.verdict !== a.verdict) return b.verdict - a.verdict;
      return (b.fit || 0) - (a.fit || 0);
    });
    return rows;
  }

  function lossReason(row, best) {
    if (row.missing) return "No cell for this class. A missing cell is missing, not permitted — route to the ruleset owner.";
    if (row.verdict === 0) return "Blocked for this data class.";
    if (row.verdict === 1 && best.verdict === 2) {
      var a = D.approver_roles[row.approver];
      return "Permitted only with sign-off" + (a ? " from the " + a.title : "") + ", so it loses to a self-service path.";
    }
    if (row.verdict === best.verdict && (row.fit || 0) < (best.fit || 0)) {
      return "Same permission, lower capability fit (" + (row.fit == null ? "n/a" : row.fit + "/5") + ", assumed).";
    }
    if (row.verdict === best.verdict) return "Equivalent permission and fit; either is defensible.";
    return "Lower permission than the recommendation.";
  }

  function dots(score) {
    var d = el("span", "dots");
    for (var i = 1; i <= 5; i++) d.appendChild(el("i", i <= score ? "on" : ""));
    return d;
  }

  function block(title, node) {
    var b = el("div", "block");
    b.appendChild(el("h3", null, title));
    b.appendChild(node);
    return b;
  }

  function route() {
    var eff = effectiveClass();
    var work = $("work").value;
    var rows = rank(eff.cls, work);
    var asked = $("plat").value;
    var best = rows[0];
    if (asked) {
      for (var q = 0; q < rows.length; q++) if (rows[q].id === asked) { best = rows[q]; break; }
    }
    var out = $("answer");
    out.textContent = "";

    /* scope warning — the error this class was added to catch */
    var sw = $("scopeWarn");
    if (eff.cls === "germline-seq") {
      sw.textContent = "";
      sw.appendChild(el("strong", null, "Scope check: this class describes what enters the prompt, not your subject. "));
      sw.appendChild(document.createTextNode(
        "Pipeline configuration, parameter choice, tool comparison and error interpretation put no sequence in the "
        + "prompt and route far lower — usually research-unpub. Somatic work is in scope where the germline travels "
        + "with it, because a tumour-normal pair contains a germline sample by construction. Public, openly consented "
        + "reference resources are not escalated."));
      sw.hidden = false;
    } else { sw.hidden = true; }

    /* destination escalation */
    var dw = $("destWarn");
    if (eff.escalatedFrom) {
      dw.textContent = "";
      dw.appendChild(el("strong", null, "Destination raised the class. "));
      dw.appendChild(document.createTextNode(
        "You selected " + eff.escalatedFrom + ", but output going to " + DEST_LABEL[eff.dest]
        + " is classified " + eff.cls + " regardless of what the input was. Routing on " + eff.cls + "."));
      dw.hidden = false;
    } else { dw.hidden = true; }

    /* jurisdiction */
    var jw = $("jurisWarn");
    var j = $("juris").value;
    if (j === "EU" || j === "UK" || j === "multi") {
      jw.textContent = "";
      jw.appendChild(el("strong", null, "No jurisdiction axis in this ruleset (open item 5). "));
      jw.appendChild(document.createTextNode(
        "The verdict below may be a US-shaped answer to an EU-shaped question. HIPAA de-identified is not GDPR "
        + "anonymous, and several de-identified clinical cells likely split by jurisdiction once the axis exists. "
        + "Confirm with the Data Protection Officer before relying on this."));
      jw.hidden = false;
    } else { jw.hidden = true; }

    if (best.missing) {
      var miss = el("div", "callout escalate");
      miss.appendChild(el("strong", null, "No cell exists for this combination. "));
      miss.appendChild(document.createTextNode("That is a gap in the ruleset, not a permission. Route to the ruleset owner."));
      out.appendChild(miss);
      return;
    }

    var anyRoute = best.verdict > 0;
    var card = el("div", "verdict " + VERDICT_CLASS[best.verdict]);

    /* head */
    var head = el("div", "verdict-head");
    var left = el("div");
    left.appendChild(el("p", "verdict-label",
      best.verdict === 2 ? "Permitted — self-service" :
      best.verdict === 1 ? "Conditional — a named role must sign" :
      "Blocked — no documented route"));
    left.appendChild(el("p", "verdict-platform",
      anyRoute || asked ? platName(best.id) : "No permitted platform"));
    head.appendChild(left);
    if (anyRoute) {
      var t = platTier(best.id);
      head.appendChild(el("span", "verdict-tier", (t ? t + " · " : "") + best.id));
    }
    card.appendChild(head);

    var body = el("div", "verdict-body");

    if (anyRoute) {
      body.appendChild(block("The rule that permits it", el("p", "rule", best.rule)));

      /* capability, never merged with permission */
      var fitWrap = el("div");
      if (best.fit != null) {
        var row = el("div", "fit-row");
        var s = el("span", "fit-score", String(best.fit));
        s.appendChild(el("small", null, "/5"));
        row.appendChild(s);
        row.appendChild(dots(best.fit));
        row.appendChild(el("span", "tag " + best.basis, best.basis));
        if (best.basis === "ASSUMED") row.appendChild(el("span", "untested", "assumed, not tested"));
        fitWrap.appendChild(row);
        if (best.note) fitWrap.appendChild(el("p", "rule", best.note));
      } else {
        fitWrap.appendChild(el("p", "rule", "No fit score recorded for this work type on this platform."));
      }
      body.appendChild(block("Capability fit for " + ucName(work).toLowerCase() + " — a separate question from permission", fitWrap));

      if (best.verdict === 1 && best.approver) {
        var a = D.approver_roles[best.approver];
        var ap = el("div", "approver");
        ap.appendChild(el("div", "who", a ? a.title : best.approver));
        ap.appendChild(el("div", "sla", a ? "SLA " + a.sla_days + " days · role, not an inbox" : ""));
        body.appendChild(block("Who signs", ap));
      }

      var cf = D.continuity_flags[best.id];
      if (cf && cf.level && cf.level !== "low" && cf.level !== "normal") {
        var cont = el("div", "continuity");
        cont.appendChild(el("b", null, "Continuity: " + cf.level));
        cont.appendChild(el("p", null, cf.text));
        body.appendChild(block("Continuity flag", cont));
      }
    } else {
      /* Blocked. Three routes, and no number. */
      var lede = el("p", "rule", best.rule);
      body.appendChild(block("Why", lede));

      var ul = el("ul", "routes");
      var red = REDUCTION[eff.cls] || { to: [], how: null };
      var lower = null;
      for (var i = 0; i < red.to.length; i++) {
        var r = rank(red.to[i], work);
        if (r[0] && !r[0].missing && r[0].verdict > 0) { lower = { cls: red.to[i], plat: r[0] }; break; }
      }
      var li1 = el("li");
      li1.appendChild(el("strong", null, "Reduce the class. "));
      if (lower) {
        li1.appendChild(document.createTextNode(
          "Reduce to " + lower.cls + " — " + red.how + " — which is "
          + (lower.plat.verdict === 2 ? "permitted" : "conditional") + " on "
          + platName(lower.plat.id) + "."));
      } else if (NO_REDUCTION_WHY[eff.cls]) {
        li1.appendChild(document.createTextNode(
          "Not available here. " + NO_REDUCTION_WHY[eff.cls]));
      } else {
        li1.appendChild(document.createTextNode(
          "No lower class with a route is reachable from " + eff.cls + " by reducing the material."));
      }
      ul.appendChild(li1);

      var enclave = null;
      rows.forEach(function (r) {
        if (!enclave && !r.missing && r.verdict > 0 && (r.id === "enclave" || r.id === "gxp")) enclave = r;
      });
      var li2 = el("li");
      li2.appendChild(el("strong", null, "Relocate the work. "));
      li2.appendChild(document.createTextNode(enclave
        ? "Move it to " + platName(enclave.id) + ", which is " +
          (enclave.verdict === 2 ? "permitted" : "conditional") + " at this class."
        : "Move it into the private research enclave or the validated instance."));
      ul.appendChild(li2);

      var li3 = el("li");
      li3.appendChild(el("strong", null, "Open an exception. "));
      var condRow = null;
      rows.forEach(function (r) { if (!condRow && r.verdict === 1 && r.approver) condRow = r; });
      var ar = condRow ? D.approver_roles[condRow.approver] : null;
      li3.appendChild(document.createTextNode(ar
        ? "Take it to the " + ar.title + ", SLA " + ar.sla_days + " days."
        : "Take it to the named approver for this class."));
      ul.appendChild(li3);
      body.appendChild(block("Three routes — an unrouted “no” becomes shadow AI", ul));

      var nc = el("p", "nocost",
        "No cost estimate is produced for a blocked path. Putting a number on a route "
        + "nobody may use is how a governance tool starts advocating for the workaround "
        + "it exists to prevent. There is no override.");
      body.appendChild(nc);
    }

    /* alternatives, each with the reason it lost */
    var tbl = el("table", "alts");
    var thead = el("thead");
    var hr = el("tr");
    ["Platform", "Verdict", "Fit", "Why it is not the recommendation"].forEach(function (h) {
      hr.appendChild(el("th", null, h));
    });
    thead.appendChild(hr); tbl.appendChild(thead);
    var tb = el("tbody");
    rows.filter(function (r) { return r.id !== best.id; }).forEach(function (r) {
      var tr = el("tr");
      tr.appendChild(el("td", "pf", platName(r.id)));
      var vt = el("td");
      if (r.missing) vt.appendChild(el("span", "pill v0", "MISSING"));
      else vt.appendChild(el("span", "pill " + VERDICT_CLASS[r.verdict],
        r.verdict === 2 ? "PERMITTED" : r.verdict === 1 ? "CONDITIONAL" : "BLOCKED"));
      tr.appendChild(vt);
      tr.appendChild(el("td", null, r.fit == null ? "—" : r.fit + "/5"));
      tr.appendChild(el("td", "why", lossReason(r, rows[0])));
      tb.appendChild(tr);
    });
    tbl.appendChild(tb);
    body.appendChild(block(anyRoute ? "Alternatives, ranked" : "Where this work can go instead", tbl));

    card.appendChild(body);
    out.appendChild(card);
  }

  /* ── matrix ────────────────────────────────────────────────────────────── */
  function renderMatrix() {
    $("cellCount").textContent = D.stats.cells;
    var t = $("matrix");
    var thead = el("thead");
    var hr = el("tr");
    hr.appendChild(el("th", null, "Data class"));
    D.platforms.forEach(function (p) { hr.appendChild(el("th", null, p.id)); });
    thead.appendChild(hr); t.appendChild(thead);

    var tb = el("tbody");
    D.data_classes.forEach(function (c) {
      var tr = el("tr");
      var th = el("th");
      th.appendChild(el("span", null, "T" + c.tier));
      th.appendChild(document.createTextNode(c.id));
      tr.appendChild(th);
      D.platforms.forEach(function (p) {
        var cell = D.matrix[p.id] ? D.matrix[p.id][c.id] : null;
        var td = el("td", cell ? VERDICT_CLASS[cell.verdict] : "");
        var b = el("button", null, cell
          ? (cell.verdict === 2 ? "PERMIT" : cell.verdict === 1 ? "COND" : "BLOCK") : "—");
        b.setAttribute("aria-pressed", "false");
        b.setAttribute("aria-label", p.id + " with " + c.id + ": " +
          (cell ? (cell.verdict === 2 ? "permitted" : cell.verdict === 1 ? "conditional" : "blocked") : "missing"));
        b.addEventListener("click", function () {
          Array.prototype.forEach.call(t.querySelectorAll("button[aria-pressed=true]"),
            function (o) { o.setAttribute("aria-pressed", "false"); });
          b.setAttribute("aria-pressed", "true");
          showCell(p.id, c.id, cell);
        });
        td.appendChild(b);
        tr.appendChild(td);
      });
      tb.appendChild(tr);
    });
    t.appendChild(tb);
  }

  function showCell(pid, cid, cell) {
    var d = $("cellDetail");
    d.textContent = "";
    var card = el("div", "cell-card");
    card.appendChild(el("h3", null, platName(pid) + " × " + className(cid)));
    card.appendChild(el("p", "coord", pid + " × " + cid + " · tier " + classTier(cid)));
    if (!cell) {
      card.appendChild(el("p", "rule", "No cell. A missing cell is a gap in the ruleset, not a permission."));
    } else {
      var lab = el("p");
      lab.appendChild(el("span", "pill " + VERDICT_CLASS[cell.verdict],
        cell.verdict === 2 ? "PERMITTED" : cell.verdict === 1 ? "CONDITIONAL" : "BLOCKED"));
      card.appendChild(lab);
      card.appendChild(el("p", "rule", cell.rule));
      if (cell.approver) {
        var a = D.approver_roles[cell.approver];
        card.appendChild(el("p", "note", "Signs: " + (a ? a.title + " · SLA " + a.sla_days + " days" : cell.approver)));
      }
    }
    d.appendChild(card);
  }

  /* ── classes ───────────────────────────────────────────────────────────── */
  function renderClasses() {
    var wrap = $("classList");
    D.data_classes.forEach(function (c) {
      var card = el("div", "class-card");
      var top = el("div", "top");
      top.appendChild(el("code", null, c.id));
      top.appendChild(el("span", "tier", "tier " + c.tier));
      card.appendChild(top);
      card.appendChild(el("p", "label", c.label));
      if (c.note) card.appendChild(el("p", "note", c.note));
      if (c.scope) {
        if (c.scope.applies_when) card.appendChild(el("p", "note", "Applies when: " + c.scope.applies_when));
        if (c.scope.somatic_and_tumour_normal) card.appendChild(el("p", "note", c.scope.somatic_and_tumour_normal));
        if (c.scope.does_not_apply_when) {
          c.scope.does_not_apply_when.forEach(function (x) {
            card.appendChild(el("p", "note", "Does not apply: " + x));
          });
        }
      }
      var counts = el("div", "counts");
      var tally = { 2: 0, 1: 0, 0: 0 };
      D.platforms.forEach(function (p) {
        var cell = D.matrix[p.id] ? D.matrix[p.id][c.id] : null;
        if (cell) tally[cell.verdict]++;
      });
      [[2, "permitted"], [1, "conditional"], [0, "blocked"]].forEach(function (pair) {
        if (tally[pair[0]]) counts.appendChild(el("span", "pill " + VERDICT_CLASS[pair[0]],
          tally[pair[0]] + " " + pair[1]));
      });
      card.appendChild(counts);
      wrap.appendChild(card);
    });
  }

  /* ── state ─────────────────────────────────────────────────────────────── */
  function renderState() {
    var s = D.stats;
    var cards = [
      ["Ruleset", D.ruleset_version, "UNSIGNED. No security, privacy, QA or legal review has occurred.", true],
      ["Cells", s.cells, s.platforms + " platforms × " + s.data_classes + " data classes.", false],
      ["Verdicts", s.permitted + " / " + s.conditional + " / " + s.blocked, "permitted / conditional / blocked.", false],
      ["Measured fit scores", (s.basis.EVIDENCE || 0) + " of " +
        ((s.basis.EVIDENCE || 0) + (s.basis.EXTERNAL || 0) + (s.basis.ASSUMED || 0)),
        "Every other score is inference from vendor documentation, tagged ASSUMED and rendered as “assumed, not tested.”", true],
      ["Reconciled", D.last_reconciled, "Target " + D.freshness_target_days + " days; distrust banner at " + D.stale_after_days + ".", false],
      ["Ruleset owner", D.owner && D.owner.name === "UNASSIGNED" ? "UNASSIGNED" : (D.owner ? D.owner.name : "—"),
        D.owner ? D.owner.role : "", true]
    ];
    var wrap = $("stateCards");
    cards.forEach(function (c) {
      var n = el("div", "card" + (c[3] ? " alarm" : ""));
      n.appendChild(el("div", "k", c[0]));
      n.appendChild(el("div", "v", String(c[1])));
      n.appendChild(el("div", "d", c[2]));
      wrap.appendChild(n);
    });

    var meanings = {
      EVIDENCE: "A local harness run against a named task pack, with a run ID and a date.",
      EXTERNAL: "A published head-to-head study, cited. An uncited one is not EXTERNAL.",
      ASSUMED: "An inference from vendor documentation. Not measured, and always labelled."
    };
    var rows = $("basisRows");
    ["EVIDENCE", "EXTERNAL", "ASSUMED"].forEach(function (k) {
      var tr = el("tr");
      tr.appendChild(el("td", null, k));
      tr.appendChild(el("td", null, meanings[k]));
      tr.appendChild(el("td", null, String(D.stats.basis[k] || 0)));
      rows.appendChild(tr);
    });
    $("basisNote").textContent =
      "Five cells previously read EXTERNAL while citing no study, and were downgraded to "
      + "ASSUMED rather than left standing. Treating an assumption as a measurement is the "
      + "most common way an enterprise AI rollout goes wrong, and a system that lets it "
      + "happen in its own data has no standing to catch it anywhere else.";
  }

  /* ── tabs ──────────────────────────────────────────────────────────────── */
  function initTabs() {
    var btns = document.querySelectorAll('.tabs button');
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(btns, function (o) {
          var on = o === b;
          o.setAttribute("aria-selected", on ? "true" : "false");
          $("panel-" + o.dataset.panel).hidden = !on;
        });
      });
    });
  }

  function initBannerLink() {
    var a = $("sketchMore");
    if (!a) return;
    a.addEventListener("click", function (e) {
      e.preventDefault();
      $("tab-state").click();
      var t = $("whatIsReal");
      if (t) t.scrollIntoView({ block: "center" });
    });
  }

  /* ── boot ──────────────────────────────────────────────────────────────── */
  fetch("data/ruleset.json")
    .then(function (r) {
      if (!r.ok) throw new Error("ruleset.json " + r.status);
      return r.json();
    })
    .then(function (data) {
      D = data;
      renderFreshness();
      populate();
      updateHints();
      renderMatrix();
      renderClasses();
      renderState();
      initTabs();
      initBannerLink();
      ["work", "dclass", "dest", "plat", "juris"].forEach(function (id) {
        $(id).addEventListener("change", function () { updateHints(); route(); });
      });
      route();
      $("buildMeta").textContent =
        "ruleset " + D.ruleset_version + " · source sha256:" + D.source_sha256_16
        + " · built " + D.generated_at.slice(0, 19).replace("T", " ") + "Z";
    })
    .catch(function (e) {
      var m = document.getElementById("answer") || document.body;
      var d = document.createElement("div");
      d.className = "callout escalate";
      d.textContent = "Could not load the ruleset (" + e.message
        + "). Without it this page has nothing to say, and it will not guess.";
      m.appendChild(d);
    });
})();
