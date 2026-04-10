# Jargon Dictionary

Quick-reference translation table. When writing a plain-English explanation, look up any technical term here before using it in the output. If the term isn't listed, apply the same pattern: name it by what it DOES, not what it's CALLED.

## Code Concepts

| Jargon | Plain English |
|---|---|
| Variable | A labeled container that holds a piece of data — like a sticky note with a name and a value |
| Function / Method | A reusable set of instructions — like a recipe you can call by name |
| Class | A blueprint for creating things that share the same structure and abilities |
| Object / Instance | A specific thing built from a blueprint |
| Array / List | An ordered collection — like a numbered list where each item has a position |
| Dictionary / Map / Hash | A lookup table — like a phone book where you find values by their label |
| String | A piece of text (the word "string" just means "a string of characters") |
| Boolean | A yes/no value — either true or false, nothing else |
| Null / Nil / Undefined / None | Empty — the data simply doesn't exist (yet or at all) |
| Type | What kind of data something is: a number, text, true/false, a list, etc. |
| Type error | The code expected one kind of data but got a different kind — like putting diesel in a gas car |
| Loop | Doing the same thing over and over for each item in a list |
| Conditional / If-else | A decision point — "if this is true, do A; otherwise, do B" |
| Callback | A set of instructions you hand to something else and say "run these when you're done" |
| Promise / Async / Await | A way to say "go do this thing, and I'll keep working while I wait for the answer" |
| Exception / Error | Something went wrong and the code stopped itself to tell you about it |
| Try-catch | A safety net — "try this risky thing, and if it fails, do this recovery step instead of crashing" |
| Recursion | A function that calls itself — like looking up a word in the dictionary and the definition uses another word you also need to look up |
| Scope | Where a piece of data is visible — like how a note on your desk is visible to you but not to someone in another room |
| Closure | A function that remembers the data from the place where it was created, even after that place is "gone" |
| Import / Require | Grabbing code from another file so you can use it here — like referencing another document |

## Architecture & Infrastructure

| Jargon | Plain English |
|---|---|
| Frontend | Everything the user sees and clicks on — the visual part of the app |
| Backend / Server | The behind-the-scenes system that processes data, talks to databases, and does the heavy thinking |
| API | A connection point where one system talks to another — like a drive-through window |
| REST API | A specific style of drive-through window where you use standard request types (get info, send info, update info, delete info) |
| GraphQL | Another style where you describe exactly what data you want and get only that — like ordering off-menu |
| Endpoint | One specific URL that does one specific thing — like one window at the DMV that only handles renewals |
| Database | Where all the data lives permanently — the app's filing system |
| SQL | The language you use to ask a database questions or tell it to store things |
| Schema | The structure/layout of how data is organized — like the column headers in a spreadsheet |
| Migration | Changing the structure of the database — like reorganizing a filing cabinet while keeping all the files |
| ORM | A translator that lets code talk to the database in its own language instead of raw SQL |
| Cache | A temporary copy of frequently-used data kept somewhere fast — like keeping a cheat sheet on your desk instead of going to the filing cabinet every time |
| CDN | Copies of your files stored on servers all over the world so users get them from the closest one — like having a warehouse in every city |
| Docker / Container | A self-contained box that has everything the app needs to run — like a portable kitchen with all utensils included |
| Environment variables | Secret settings stored outside the code — like keeping passwords in a safe rather than written on a whiteboard |
| Microservice | Breaking one big app into many small specialized apps that talk to each other |
| Monolith | One big app that does everything in one place |
| Load balancer | A traffic cop that sends incoming users to whichever server is least busy |
| Serverless | Code that runs only when triggered and you only pay for the seconds it runs — no permanent server to maintain |
| Webhook | An automatic notification — "when X happens, immediately tell this URL about it" |

## Development Workflow

| Jargon | Plain English |
|---|---|
| Repository / Repo | The master folder for a project, including its entire change history |
| Commit | Saving a snapshot of your work with a description of what changed |
| Branch | A parallel copy of the project where you can make changes without affecting the main version |
| Merge | Combining changes from one branch into another |
| Pull request / PR | A formal request to merge your changes, where others can review them first |
| Conflict | Two people changed the same thing differently and the system can't figure out which version to keep |
| CI/CD | Automatic checking and deploying — every time you save changes, a robot tests them and (if they pass) publishes them |
| Pipeline | A sequence of automated steps that code goes through from "I wrote it" to "users can see it" |
| Linting | Automatic style-checking for code — like spell-check but for formatting and common mistakes |
| Build | Converting source code into the final form that actually runs — like compiling a manuscript into a printed book |
| Bundle | Packing many files into fewer files so they load faster in a browser |
| Deploy | Publishing the app so real users can access it |
| Staging | A test version of the live app where you can check things before real users see them |
| Production / Prod | The real, live version that actual users are using right now |
| Hot reload | The app updates instantly as you edit code — no need to restart or refresh |
| Dependency | Another piece of software your project relies on — like ingredients in a recipe |
| Package manager (npm, pip, etc.) | A tool that downloads and manages dependencies — like a grocery delivery service for code ingredients |
| Lock file | A receipt that records the exact version of every dependency — so everyone building the project gets identical ingredients |

## iOS / Swift Specific

| Jargon | Plain English |
|---|---|
| SwiftUI View | A piece of the screen — a button, a list, a card, a whole page |
| State / @State | Data that, when it changes, automatically updates what's shown on screen |
| Binding / @Binding | A shared reference to data — two screens looking at the same piece of paper |
| Observable / @Observable | An object that announces when its data changes so the screen can refresh |
| Modifier | An instruction that changes how a view looks or behaves — like ".bold()" on text |
| NavigationStack | The system that manages moving between screens (pushing forward, going back) |
| Simulator | A fake iPhone/iPad running on your Mac for testing |
| TestFlight | Apple's system for sending beta versions of your app to testers |
| Provisioning profile | Apple's permission slip that says "this app is allowed to run on these devices" |
| Entitlement | A specific capability your app has been approved to use (push notifications, iCloud, etc.) |
| Xcode | The app you use to build iPhone/Mac apps — Apple's version of a code editor |
| Target | A specific thing Xcode is building — the app itself, a test suite, or an extension |
| Scheme | The set of instructions for how to build, run, and test a specific target |
| Info.plist | A settings file that tells iOS basic facts about your app (name, version, what permissions it needs) |

## Error Messages (Common Patterns)

| Error pattern | What it actually means |
|---|---|
| "Cannot find X in scope" | The code references something that doesn't exist here — either it was never created, or it's in a different file that hasn't been connected |
| "Type mismatch" / "Expected X, got Y" | The code is trying to put the wrong kind of data somewhere — like trying to use text where a number is required |
| "Index out of range" | The code tried to access item #10 in a list that only has 7 items |
| "Nil / null reference" | The code tried to use data that doesn't exist yet — the container is empty |
| "Permission denied" | The app or tool doesn't have the right access level to do what it's trying to do |
| "Connection refused" | The code tried to talk to a server that either isn't running or isn't accepting connections |
| "Timeout" | The code waited too long for a response and gave up |
| "Module not found" / "No such module" | A required dependency isn't installed or can't be located |
| "Build failed" | The code couldn't be converted into a running app — there are errors that need to be fixed first |
| "Deprecated" | This feature still works but is being phased out — it'll stop working in a future update |
