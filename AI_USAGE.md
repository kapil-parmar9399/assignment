# AI usage record

This record is based on the Codex work visible in this chat. Review it and correct anything that does not match your own account of the assignment. This summary is not the required genuine transcript.

## AI tools used

- OpenAI Codex (GPT-6) in the project workspace. It inspected the assignment and project, wrote application and documentation files, and ran Django commands.

## Prompts and tasks

These are selected excerpts from the actual requests, followed by brief summaries. They are not a transcript:

- Initial request: “You are helping me complete a Python/Django hiring assignment titled ‘AI-Assisted Box Selection System’. IMPORTANT: Follow the original assignment document exactly. Do not invent requirements or build an unrelated project.” The request also instructed Codex to read the assignment, explain its requirements, and wait for approval before implementation. It specified fit and rotation checks, weight limits, cost-based selection, tests, and submission files.
- Approval: “Approved. Proceed with the implementation according to the plan. Build the complete Django project in the current workspace, create the required files, and run the tests.”
- Bug report: “There is a bug in my Boxwise Django project. I changed the Book product's weight to 6 kg in Django Admin. Small Box has a maximum weight capacity of 5 kg, but the website still recommends Small Box.” The rest of that request asked Codex to fix the root cause, add regression tests for the 6 kg/5 kg case and a suitable box, and report actual test results.
- Documentation task (provided in the pasted text): “I have an existing Django project for my Python/Django developer assignment. The project is working, and I do not want any changes to the existing application or its functionality.” The task then asked for an audit and completion of truthful submission documents while preserving application code and not fabricating the transcript or personal reflection.

The original prompts remain in the actual conversation. Use the instructions in `AI_TRANSCRIPT_INSTRUCTIONS.md` to obtain the required genuine transcript; do not treat this summary as one.

## Output accepted, changed, or not used

The project includes AI-generated Django code and documentation, including models, a recommendation service, views, templates, tests, and setup documentation. The recommendation design checks axis-aligned rotations and product overlap, sums weight by quantity, and selects the least-cost box that passes the fit and weight checks.

Testing found two bugs during development. The initial packing implementation read dimensions from an order line instead of its product. A later regression investigation found that a cached related product could carry an outdated weight; the service was changed to reload products from the database. The tests were updated to cover these cases.

No AI-generated transcript is included. `What_Did_I_Learn.md` is a clearly labelled draft for personal review, not a claim about what the submitter personally learned. Rewrite it in your own words before using it, as required by the assignment.

## Mistakes found

- The first packing implementation accessed dimensions on the order line; tests exposed the error, and the code was corrected to use the product.
- A cached product instance could carry a stale weight after a database update; the recommendation service now reloads product records, and regression tests cover the 6 kg product and 5 kg box case.

## Verification

The latest recorded test run used `python manage.py test` on Python 3.14.3 and Django 6.0.3. It reported 15 tests and `OK`; see `TEST_OUTPUT.md` for the recorded output. `python manage.py check` reported no issues. These are Codex-run results, not a claim that the submitter independently ran or reviewed them. No GitHub Actions run was verified.
