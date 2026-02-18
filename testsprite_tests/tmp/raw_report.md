
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
  File "<string>", line 52, in <module>
  File "<string>", line 21, in test_post_auth_register_user_registration_with_valid_data
AssertionError: Expected 201 Created, got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/035769d6-7665-4428-ada5-91d04f0b165d
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 post auth login user login with valid credentials
- **Test Code:** [TC002_post_auth_login_user_login_with_valid_credentials.py](./TC002_post_auth_login_user_login_with_valid_credentials.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 34, in <module>
  File "<string>", line 21, in test_post_auth_login_valid_credentials
AssertionError: Expected status 200, got 404, response: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/fa54a43e-790d-4c4a-bc7c-42cce38cac0c
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 get auth me fetch current user information
- **Test Code:** [TC003_get_auth_me_fetch_current_user_information.py](./TC003_get_auth_me_fetch_current_user_information.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 64, in <module>
  File "<string>", line 28, in test_get_auth_me_fetch_current_user_information
  File "/var/task/requests/models.py", line 1024, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://localhost:8000/auth/register

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/6274460e-df89-4866-8ab6-1a730988a0e2
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 post auth refresh refresh access token using refresh token
- **Test Code:** [TC004_post_auth_refresh_refresh_access_token_using_refresh_token.py](./TC004_post_auth_refresh_refresh_access_token_using_refresh_token.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 64, in <module>
  File "<string>", line 26, in test_post_auth_refresh_refresh_access_token_using_refresh_token
AssertionError: User registration failed: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/e8e51351-6245-4d6b-84d0-303508198a59
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 post auth logout invalidate refresh token on logout
- **Test Code:** [TC005_post_auth_logout_invalidate_refresh_token_on_logout.py](./TC005_post_auth_logout_invalidate_refresh_token_on_logout.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 56, in <module>
  File "<string>", line 28, in test_post_auth_logout_invalidate_refresh_token_on_logout
AssertionError: Login failed: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/44327208-3f98-4e2b-b86f-ebc6ac367b17
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 post users create new user with valid data
- **Test Code:** [TC006_post_users_create_new_user_with_valid_data.py](./TC006_post_users_create_new_user_with_valid_data.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 43, in <module>
  File "<string>", line 23, in test_post_users_create_new_user_with_valid_data
AssertionError: Expected status 201, got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/03c66b8a-771f-47a9-9620-5c20c4fc314c
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 delete users delete user by id
- **Test Code:** [TC007_delete_users_delete_user_by_id.py](./TC007_delete_users_delete_user_by_id.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 34, in <module>
  File "<string>", line 15, in test_delete_user_by_id
AssertionError: User creation failed with status 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/702a0a3d-1be6-4619-8cd9-1ff0c56d1e4b
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 get api workspaces list all workspaces for authenticated user
- **Test Code:** [TC008_get_api_workspaces_list_all_workspaces_for_authenticated_user.py](./TC008_get_api_workspaces_list_all_workspaces_for_authenticated_user.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 115, in <module>
  File "<string>", line 38, in test_get_api_workspaces_list_all_workspaces_for_authenticated_user
AssertionError: Login failed with status 404, body: {"error":"Route not found"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/4a3cded7-1c84-4f14-8ec0-acfc8b97eced
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009 post api invitations send invitation to join workspace
- **Test Code:** [TC009_post_api_invitations_send_invitation_to_join_workspace.py](./TC009_post_api_invitations_send_invitation_to_join_workspace.py)
- **Test Error:** Traceback (most recent call last):
  File "<string>", line 20, in get_access_token
  File "/var/task/requests/models.py", line 1024, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: http://localhost:8000/auth/login

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 101, in <module>
  File "<string>", line 50, in test_post_api_invitations_send_invitation_to_join_workspace
  File "<string>", line 24, in get_access_token
RuntimeError: Failed to login and get access token: 404 Client Error: Not Found for url: http://localhost:8000/auth/login

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/e8ae559b-184b-4a43-9b6e-16fa970cc984
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010 get root health check endpoint
- **Test Code:** [TC010_get_root_health_check_endpoint.py](./TC010_get_root_health_check_endpoint.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 22, in <module>
  File "<string>", line 8, in test_tc010_get_root_health_check_endpoint
AssertionError: Expected status 200, got 404

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/48a07169-d9da-4909-bf1f-9d6986f9dc59/b8c06c8b-ab35-4a80-915c-23ddf41bcb38
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **0.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---