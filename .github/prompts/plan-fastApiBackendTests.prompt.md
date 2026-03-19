## Plan: FastAPI Backend Tests

Add backend API tests under a dedicated tests directory using `pytest` and FastAPI’s `TestClient`. The recommended approach is to install `pytest`, create isolated fixtures so each test starts from a clean copy of the in-memory activities data, and cover the current backend behavior only: listing activities, signing up, duplicate signup rejection, unregistering, and unregister error cases.

**Steps**
1. Phase 1: Prepare the test setup.
2. Add `pytest` to `/workspaces/skills-getting-started-with-github-copilot/requirements.txt` so the repo and the exercise workflow both recognize the test runner.
3. Confirm `/workspaces/skills-getting-started-with-github-copilot/pytest.ini` still provides the correct import path for `src.app`; only extend it if test discovery or markers need configuration.
4. Create `/workspaces/skills-getting-started-with-github-copilot/tests/` as the dedicated backend test directory.
5. Phase 2: Build shared test fixtures. Depends on 1-4.
6. Add `/workspaces/skills-getting-started-with-github-copilot/tests/conftest.py` with a `TestClient` fixture and a fixture that resets `src.app.activities` to a deep-copied baseline before each test so tests do not leak state into one another.
7. Keep the fixture strategy minimal by reusing the existing global `app` object from `/workspaces/skills-getting-started-with-github-copilot/src/app.py`; only refactor `/workspaces/skills-getting-started-with-github-copilot/src/app.py` if resetting the module-level `activities` dict proves awkward in implementation.
8. Phase 3: Add endpoint test modules. Parallel after 6-7.
9. Create `/workspaces/skills-getting-started-with-github-copilot/tests/test_activities.py` for `GET /activities`, covering status code `200`, expected top-level activity names, and representative response shape for one activity.
10. Create `/workspaces/skills-getting-started-with-github-copilot/tests/test_signup.py` for `POST /activities/{activity_name}/signup`, covering successful signup, participant added to the selected activity, unknown activity returns `404`, and duplicate signup returns `400`.
11. Create `/workspaces/skills-getting-started-with-github-copilot/tests/test_unregister.py` for `DELETE /activities/{activity_name}/signup`, covering successful unregister, participant removed from the selected activity, unknown activity returns `404`, and removing a non-enrolled participant returns `404`.
12. Structure each test using the AAA pattern explicitly in the body: arrange input/state, act with the client request, assert status code and mutated activity state.
13. Phase 4: Verify and tighten scope. Depends on 9-12.
14. Run `pytest` and fix only issues directly related to backend testability or deterministic state reset.
15. If imports or state setup fail, make the smallest production-code adjustment necessary in `/workspaces/skills-getting-started-with-github-copilot/src/app.py`, such as extracting a reusable initial-data factory for the fixture to call.

**Relevant files**
- `/workspaces/skills-getting-started-with-github-copilot/requirements.txt` — add `pytest`.
- `/workspaces/skills-getting-started-with-github-copilot/pytest.ini` — keep or minimally extend test discovery/import settings.
- `/workspaces/skills-getting-started-with-github-copilot/src/app.py` — reuse the FastAPI `app` object and current `activities` store; only touch if fixture isolation needs a small helper.
- `/workspaces/skills-getting-started-with-github-copilot/tests/conftest.py` — centralize `TestClient` and test-state reset fixtures.
- `/workspaces/skills-getting-started-with-github-copilot/tests/test_activities.py` — cover list endpoint behavior.
- `/workspaces/skills-getting-started-with-github-copilot/tests/test_signup.py` — cover signup success and validation failures.
- `/workspaces/skills-getting-started-with-github-copilot/tests/test_unregister.py` — cover unregister success and validation failures.
- `/workspaces/skills-getting-started-with-github-copilot/.github/steps/4-step.md` — repo guidance indicating `pytest` and a separate `tests/` directory are expected.

**Verification**
1. Install dependencies from `requirements.txt` in the project environment.
2. Run `pytest` from `/workspaces/skills-getting-started-with-github-copilot` and confirm all backend tests pass.
3. Re-run a signup test and an unregister test together to confirm fixture isolation prevents shared-state flakiness.
4. Optionally hit `GET /activities` manually after the test run to ensure the in-memory seed data is restored for normal app use.

**Decisions**
- Included scope: backend FastAPI endpoint tests only, under a top-level `tests/` directory.
- Included scope: `pytest` in `requirements.txt`, because the repo exercise explicitly checks for it.
- Included scope: AAA-style test structure.
- Excluded scope: frontend tests, browser tests, and unrelated backend feature changes.
- Excluded scope: capacity-limit tests for signup, because the current backend does not enforce `max_participants`; tests should codify current behavior unless that feature is separately requested.
- Recommended implementation detail: prefer fixture-based reset over broad refactoring of production code.

**Further Considerations**
1. If you want stricter organization, split the tests further by success and error cases, but the three-file layout above is likely the best balance for this repo.
2. If implementation exposes awkward state coupling, introduce a small `create_initial_activities()` helper in `/workspaces/skills-getting-started-with-github-copilot/src/app.py` rather than more invasive app restructuring.
