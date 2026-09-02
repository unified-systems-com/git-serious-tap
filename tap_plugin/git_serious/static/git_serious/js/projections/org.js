/**
 * git-serious ORG-VIEW layout (a copy of the landing layout, split out 2026-09-02 so the two evolve separately) — the observed account's CI/CD system as one
 * legible picture (git-serious-tap#6, req-git-serious-status-wall).
 *
 * Structure is drawn as containment, not as edges: the account is a box, each
 * repository is a box inside it, each workflow is a card inside its repository.
 * The GitHub Apps sit in a row beneath the
 * account; their ENABLED_ON edges into the repositories stay visible because
 * "which apps touch which repos" is a real question. Runs are not on the
 * canvas — they arrive as status badges on the workflow cards, populated by
 * the projection's status_badges searches (a page and a query, per the
 * overlay-consensus build rule).
 *
 * Standard tap layout module: `export async function execute(context)`
 * (spec-viz-layouts.md, req-viz-layout-module-contract).
 */

import {projectNested} from "/static/tap_viz/js/runtime/nested-projection.js";

const T = {
    platform: "github_core__github_platform",
    account: "github_core__github_account",
    repository: "github_core__github_repository",
    workflow: "github_core__github_workflow",
    app: "github_core__github_app",
    runner: "github_core__github_runner",
};

// Leaf card sizes are chosen to hold a name, not just an icon; containers
// take these as floors and grow to their children (spec-viz-nested-projection,
// natural sizing).
const BASE_SIZES = {
    [T.platform]: {width: 480, height: 200},
    [T.account]: {width: 320, height: 120},
    [T.repository]: {width: 290, height: 70},  // floor wide enough for a 15px "owner/repo" label over a single card
    [T.workflow]: {width: 190, height: 40},
    [T.app]: {width: 180, height: 40},
    [T.runner]: {width: 180, height: 40},
};

// github_core carries no platform → app edge (apps hang off repositories via
// ENABLED_ON and off the account via installations), so the org view
// synthesizes one per app in the scene to nest the apps row inside the
// github.com box. Scene-local: never written to the grid. The durable fix
// is a HOSTS_APP edge minted by the collector (filed against github_core).
const HOSTS_APP_EDGE = "_ORG_VIEW_HOSTS_APP";

export async function execute(context) {
    const {cy, trigger_reason} = context;

    const platform = cy.nodes(`[entity_type = "${T.platform}"]`).first();
    if (platform.nonempty()) {
        const synthesized = [];
        cy.nodes(`[entity_type = "${T.app}"]`).forEach((app) => {
            const id = `${HOSTS_APP_EDGE}:${app.id()}`;
            if (cy.getElementById(id).empty()) {
                synthesized.push({group: "edges", data: {id, source: platform.id(), target: app.id(), label: HOSTS_APP_EDGE, edge_type: HOSTS_APP_EDGE}});
            }
        });
        if (synthesized.length > 0) cy.add(synthesized);
    }

    // Edge-type labels are noise at this altitude: containment carries the
    // structure and the only free-standing edges are the apps' ENABLED_ON
    // lines, whose meaning is the line itself.
    cy.style()
        // Edge labels off; edges drawn ABOVE the compound boxes — with every node
        // inside the opaque github.com container the default edge depth would
        // paint the apps' ENABLED_ON lines underneath it.
        .selector("edge")
        .style({label: "", "z-compound-depth": "top", "z-index": 1})
        .selector("node")
        .style({"font-size": "14px"})
        .selector(".tap-viewport-parent")
        .style({"font-size": "15px", "font-weight": "600", "text-margin-y": 8})
        .selector(`node[entity_type = "${T.workflow}"], node[entity_type = "${T.app}"], node[entity_type = "${T.runner}"]`)
        .style({"font-size": "14px", "text-wrap": "ellipsis", "text-max-width": "170px", "text-valign": "center", "text-halign": "center"})
        .update();

    // Repositories sit inside their owner's box, so the "owner/" prefix on
    // every label is redundant and is what pushed the long names past their
    // boxes. Strip it for display only (the entity name is untouched).
    cy.nodes(`[entity_type = "${T.repository}"]`).forEach((repo) => {
        const label = repo.data("label") || "";
        const slash = label.indexOf("/");
        if (slash > 0) repo.data("label", label.slice(slash + 1));
    });

    await projectNested(cy, {
        relationships: [
            {
                name: "platform-hosts-account",
                gryphon: `(parent:${T.platform})-[:HOSTS_ACCOUNT__github_core]->(child:${T.account})`,
            },
            {
                name: "platform-hosts-app",
                gryphon: `(parent:${T.platform})-[:${HOSTS_APP_EDGE}]->(child:${T.app})`,
            },
            {
                name: "account-owns-repository",
                gryphon: `(parent:${T.account})-[:OWNS_REPO__github_core]->(child:${T.repository})`,
            },
            {
                name: "repository-defines-workflow",
                gryphon: `(parent:${T.repository})-[:DEFINES_WORKFLOW__github_core]->(child:${T.workflow})`,
            },
        ],
        baseSizes: BASE_SIZES,
        padding: 14,
        paddings: {[T.account]: 34, [T.platform]: 40},
        // github.com is the one root. Inside it the account box sits above
        // the apps row (tiers); repositories tile inside the account;
        // workflows tile inside their repository.
        innerLayout: {
            name: "tiered-rows",
            rowGap: 48,
            itemGap: 18,
            tiers: [
                {name: "account", entityTypes: [T.account]},
                {name: "apps", entityTypes: [T.app, T.runner]},
            ],
        },
        innerLayouts: {
            // Repositories vary from two workflows to twenty-five; a wrapping
            // variable-cell flow keeps the account box compact (tap#292).
            [T.account]: {name: "flow", aspect: 2.0, gap: 18, sort: "area-desc"},
            [T.repository]: {name: "grid", spacing: 1.1},
        },
    });

    // Framing on initial load is owned by the projection runtime (it fits
    // after badges are placed); re-entries keep the viewer's viewport.
    void trigger_reason;
}
