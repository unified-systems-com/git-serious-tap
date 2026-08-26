# git-serious

**CI/CD configuration is impossible to see all at once — and getting it wrong is catastrophic.**

**Visualize, track, and secure your CI/CD system — for humans and agents.**

> **Status: pre-alpha.** git-serious is being built in the open, first against our own
> CI/CD system. Nothing below is installable yet; the roadmap is in this repo's milestones.

## Why

Building, maintaining, and securing a modern CI/CD system is complicated, and the complexity
is the bad kind: it isn't in one place. It's strewn across workflow files, branch rulesets,
environments, org settings, the bots and apps wired into your repos, the third-party services
they talk to — and don't get me started on PATs. No single screen shows you all of it, so
nobody actually knows what it is. That's the worst of all worlds, and it sits on the most
critical of critical paths: the one that ships your software.

## What git-serious does

1. **Pulls your running CI/CD system onto the grid** — repos, pipelines, runs, rules, apps,
   credentials, and the relationships between them, as one connected picture.
2. **Presents exactly the pages, views, and affordances you need** to understand it — built
   to be read by people and by the agents working alongside them.
3. **Tracks how that configuration and its operations change over time**, so "what changed?"
   is a question with an answer.
4. **Enables automated, agent-driven security review** that finds issues and helps you fix
   them.
5. **Does all of it with down-scoped, read-only access** — it observes your system; it can
   never be the thing that breaks it.

## Running it

1. Clone the repo.
2. Run the install / configure skill.
3. Tailor it to your liking.

## Key concepts

**Master complexity.** git-serious distills what you actually need to know so you can master
your CI/CD system instead of being mastered by it.

**Software as a sophisticated beanbag.** Adjust it yourself. Your own plugins add pages,
views, collectors — whatever you need to understand *your* system. git-serious ships with
GitHub Actions; extending it to another forge, or to the particular shape of your pipeline,
is what it's built for.

**The grid.** Underneath is the data model at the heart of
[the Analogy Platform](https://github.com/unified-systems-com/tap): it tracks, associates,
and presents the pieces of your system the way you — and your agents — need to see them.
