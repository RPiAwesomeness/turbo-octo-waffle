# General
- Very quick and easy to spin up API
- Less verbose than Flask, though not by much

# FastAPI
- Errors from pydantic aren't always the clearest
  - Ran into issue where a response didn't match the `response_model` and it just told me that `value was invalid dict` without providing a helpful traceback/info to trace the point of the invalid response
- `/example/` and `/example` are considered separate. Starlette (ASGI framework FastAPI is based on) will redirect `/example/` to `/example` but unless you add a decorator for both it's a redirect instead of just being automatically handled by the same handler:
  ```python
  @app.get("/example")
  @app.get("/example/")
  def test_get():
    return {}
  ```
- Can have optional values in response. If they aren't set explicitly in the return value they can be stripped if the `response_model_exclude_unset` arg is set to `True` but can still be included if explicitly set to `None` in the response dictionary.

# Transitioning