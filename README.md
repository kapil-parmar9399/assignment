# AI-Assisted Box Selection System

A small Django application for recommending the least-cost available shipping box that can physically contain an order while staying within the box's weight limit.

## Requirements

- Python 3.10 or newer
- pip

## Install and run

From the project folder:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/>. The admin site is at <http://127.0.0.1:8000/admin/>. Add products and available boxes in admin, then return to the home page to make a recommendation. The order form applies one quantity to each selected product; the admin can record distinct quantities on order lines.

The included settings are for local development. Before deployment, set `DJANGO_SECRET_KEY` to a private random value, set `DJANGO_DEBUG=false`, and set `DJANGO_ALLOWED_HOSTS` to the actual comma-separated hostnames.

## Recommendation approach

The recommendation service expands order quantities, sums product weights, and evaluates each available box. It searches product rotations along the three box axes and checks each candidate placement against box boundaries and every already placed product. This avoids treating volume alone as proof of fit. Among eligible boxes, it selects the lowest cost; equal-cost boxes are ordered by volume and name for predictable results. If no box qualifies, the interface reports that no suitable box was found.

This is a practical backtracking orthogonal packing search for small orders. It assumes rigid rectangular products, axis-aligned rotations, no extra padding, and that products may touch but may not overlap. It does not account for cushioning, fragile-item constraints, stacking strength, box wall thickness, or packing labor. Larger orders can make the search expensive; production use would need performance limits and operational packing rules.

## Tests and checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Recorded run output is in [TEST_OUTPUT.md](TEST_OUTPUT.md). A GitHub Actions workflow runs checks and tests on pushes and pull requests.

## Submission items to complete

- Push this project to GitHub and provide the real repository link.
- Export the genuine AI chat transcript yourself and include it in the repository. Do not generate or reconstruct it; see [AI_TRANSCRIPT_INSTRUCTIONS.md](AI_TRANSCRIPT_INSTRUCTIONS.md).
- Write your own response to “What did you learn in this assignment?” based on your experience. [What_Did_I_Learn.md](What_Did_I_Learn.md) is only a draft to review and personalize; do not submit it unchanged.
- Complete [AI_USAGE.md](AI_USAGE.md) from your actual tool use, prompts, decisions, mistakes found, and verification.
