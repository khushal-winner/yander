
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** yander
- **Date:** 2026-02-18
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001 post auth register user registration with valid data
- **Test Code:** [TC001_post_auth_register_user_registration_with_valid_data.py](./TC001_post_auth_register_user_registration_with_valid_data.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 58, in <module>
  File "<string>", line 23, in test_post_auth_register_user_registration_with_valid_data
AssertionError: Expected 201, got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/d21cdd75-cd0f-49b7-a589-5dd3120c58cd
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 post auth login user login with valid credentials
- **Test Code:** [TC002_post_auth_login_user_login_with_valid_credentials.py](./TC002_post_auth_login_user_login_with_valid_credentials.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 22, in <module>
  File "<string>", line 15, in test_post_auth_login_valid_credentials
AssertionError: Expected status 200 but got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/b5ececc6-2850-4296-8df0-4a872e337d91
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 get auth me fetch current user information
- **Test Code:** [TC003_get_auth_me_fetch_current_user_information.py](./TC003_get_auth_me_fetch_current_user_information.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 29, in test_get_auth_me_fetch_current_user_information
  File "/var/task/requests/models.py", line 1024, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://localhost:8000/auth/register

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 72, in <module>
  File "<string>", line 32, in test_get_auth_me_fetch_current_user_information
AssertionError: Registration request failed: 404 Client Error: Not Found for url: http://localhost:8000/auth/register

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/081608cf-08a2-44d0-8475-76148f3d1129
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 post auth refresh refresh access token using refresh token
- **Test Code:** [TC004_post_auth_refresh_refresh_access_token_using_refresh_token.py](./TC004_post_auth_refresh_refresh_access_token_using_refresh_token.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 39, in <module>
  File "<string>", line 20, in test_post_auth_refresh
AssertionError: Login failed: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/bf672d06-1001-4480-8acb-2bb448a2e588
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 post auth logout invalidate refresh token on logout
- **Test Code:** [TC005_post_auth_logout_invalidate_refresh_token_on_logout.py](./TC005_post_auth_logout_invalidate_refresh_token_on_logout.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 20, in test_post_auth_logout_invalidate_refresh_token
  File "/var/task/requests/models.py", line 1024, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://localhost:8000/auth/register

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 60, in <module>
  File "<string>", line 22, in test_post_auth_logout_invalidate_refresh_token
AssertionError: User registration request failed: 404 Client Error: Not Found for url: http://localhost:8000/auth/register

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/1a4c88cc-8252-49d9-b8cf-886481e8c102
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 post users create new user with valid data
- **Test Code:** [TC006_post_users_create_new_user_with_valid_data.py](./TC006_post_users_create_new_user_with_valid_data.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 35, in <module>
  File "<string>", line 20, in test_post_users_create_new_user_with_valid_data
AssertionError: Expected status code 201 but got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/b2d83aa1-b713-4725-a9af-2f93c08656b8
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 delete users delete user by id
- **Test Code:** [TC007_delete_users_delete_user_by_id.py](./TC007_delete_users_delete_user_by_id.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 42, in <module>
  File "<string>", line 19, in test_delete_user_by_id
AssertionError: User creation failed: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/0d881d26-4cd6-4dd2-a341-c9979877ab7b
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 get api workspaces list all workspaces for authenticated user
- **Test Code:** [TC008_get_api_workspaces_list_all_workspaces_for_authenticated_user.py](./TC008_get_api_workspaces_list_all_workspaces_for_authenticated_user.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 215, in <module>
  File "<string>", line 36, in test_get_api_workspaces_list_all_workspaces
AssertionError: Login failed: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/03271ee5-4156-4ad4-995f-3f921f61c8c8
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009 post api invitations send invitation to join workspace
- **Test Code:** [TC009_post_api_invitations_send_invitation_to_join_workspace.py](./TC009_post_api_invitations_send_invitation_to_join_workspace.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 17, in get_access_token
  File "/var/task/requests/models.py", line 1024, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://localhost:8000/auth/login

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 81, in <module>
  File "<string>", line 51, in test_post_api_invitations_send_invitation
  File "<string>", line 28, in get_access_token
  File "/var/task/requests/models.py", line 1024, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://localhost:8000/auth/register

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/edc330bb-537e-424c-8128-0af90adf5c75
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010 get root health check endpoint
- **Test Code:** [TC010_get_root_health_check_endpoint.py](./TC010_get_root_health_check_endpoint.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/d6731a4a-ad42-456b-b09c-5bae7d109df4/75320008-7d58-48f9-905d-db54d867dc98
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **10.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---