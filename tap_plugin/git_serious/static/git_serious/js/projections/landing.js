/**
 * git-serious landing layout — the observed account's CI/CD system as one
 * legible picture (git-serious-tap#6, req-git-serious-status-wall).
 *
 * Structure is drawn as containment, not as edges: the account is a box, each
 * repository is a box inside it, each workflow is a card inside its repository.
 * The GitHub Apps (and the Actions OIDC issuer) sit in a row beneath the
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
    issuer: "identity_core__oidc_issuer",
};

// Leaf card sizes are chosen to hold a name, not just an icon; containers
// take these as floors and grow to their children (spec-viz-nested-projection,
// natural sizing).
const BASE_SIZES = {
    [T.platform]: {width: 140, height: 36},
    [T.account]: {width: 320, height: 120},
    [T.repository]: {width: 180, height: 64},
    [T.workflow]: {width: 160, height: 34},
    [T.app]: {width: 150, height: 34},
    [T.runner]: {width: 150, height: 34},
    [T.issuer]: {width: 170, height: 34},
};

export async function execute(context) {
    const {cy, trigger_reason} = context;

    // Edge-type labels are noise at this altitude: containment carries the
    // structure and the only free-standing edges are the apps' ENABLED_ON
    // lines, whose meaning is the line itself.
    cy.style()
        .selector("edge")
        .style({label: ""})
        .selector(`node[entity_type = "${T.workflow}"], node[entity_type = "${T.app}"], node[entity_type = "${T.issuer}"]`)
        .style({"text-wrap": "ellipsis", "text-max-width": "140px", "text-valign": "center", "text-halign": "center"})
        .update();

    await projectNested(cy, {
        relationships: [
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
        padding: 12,
        paddings: {[T.account]: 30},
        // Roots (platform, the account box, apps, issuer) stack top-to-bottom
        // in tiers; repositories tile inside the account; workflows tile
        // inside their repository.
        innerLayout: {
            name: "tiered-rows",
            rowGap: 40,
            itemGap: 16,
            tiers: [
                {name: "platform", entityTypes: [T.platform]},
                {name: "account", entityTypes: [T.account]},
                {name: "apps", entityTypes: [T.app, T.issuer, T.runner]},
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
