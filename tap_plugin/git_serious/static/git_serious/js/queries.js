/* git-serious query pack — client-side filter for the pack list (spec-git-serious-query-pack).
   Content only: rows carry data-status / data-text; chips and tiles set the status filter, the search box
   narrows by text. Group headers hide when every row beneath them is hidden; the live count says what is
   shown so an empty list is a stated state, never a blank. */
(function () {
  "use strict";
  var root = document.getElementById("tap-gs-pack");
  if (!root) return;
  var rows = Array.prototype.slice.call(root.querySelectorAll("tr.tap-gs-pack__row"));
  var groups = Array.prototype.slice.call(root.querySelectorAll("tr.tap-gs-pack__group"));
  var chips = Array.prototype.slice.call(root.querySelectorAll(".tap-gs-chip"));
  var tiles = Array.prototype.slice.call(root.querySelectorAll(".tap-gs-tile"));
  var search = root.querySelector("#tap-gs-pack-search");
  var count = root.querySelector("#tap-gs-pack-count");
  var none = root.querySelector("#tap-gs-pack-none");
  var status = "all";

  function apply() {
    var text = (search && search.value ? search.value : "").trim().toLowerCase();
    var shown = 0;
    var perGroup = {};
    rows.forEach(function (tr) {
      var ok = (status === "all" || tr.getAttribute("data-status") === status) &&
        (!text || (tr.getAttribute("data-text") || "").indexOf(text) !== -1);
      tr.hidden = !ok;
      if (ok) {
        shown += 1;
        var g = tr.getAttribute("data-stage");
        perGroup[g] = (perGroup[g] || 0) + 1;
      }
    });
    groups.forEach(function (tr) {
      var g = tr.getAttribute("data-stage");
      var n = perGroup[g] || 0;
      tr.hidden = n === 0;
      var c = tr.querySelector(".tap-gs-pack__gcount");
      if (c) c.textContent = String(n);
    });
    if (count) count.textContent = shown + " of " + rows.length + " shown";
    if (none) none.hidden = shown !== 0;
    chips.forEach(function (b) { b.classList.toggle("is-active", b.getAttribute("data-filter") === status); });
    tiles.forEach(function (t) { t.classList.toggle("is-active", t.getAttribute("data-filter") === status); });
  }

  chips.forEach(function (b) {
    b.addEventListener("click", function () { status = b.getAttribute("data-filter") || "all"; apply(); });
  });
  tiles.forEach(function (t) {
    t.addEventListener("click", function () {
      var f = t.getAttribute("data-filter");
      status = (status === f) ? "all" : f;
      apply();
    });
  });
  if (search) search.addEventListener("input", apply);
  apply();
})();
