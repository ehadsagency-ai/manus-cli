# Bugs Found During End-to-End Testing

## Critical Bugs (Blocking)

### 1. ❌ CLI calls non-existent `chat_stream()` method
**Location**: `cli_v4.py`  
**Issue**: CLI tries to call `client.chat_stream()` but API client only has `stream_task()`  
**Impact**: Chat command completely broken  
**Fix**: Update CLI to use `client.stream_task()` and `client.create_task()`

### 2. ❌ Roles command shows wrong field
**Location**: `cli_v4.py` line 125  
**Issue**: Tries to access `role_info["description"]` but roles dict has `role_info["name"]`  
**Impact**: Roles command crashes  
**Fix**: Change to use `role_info["name"]` or add "description" field to roles

## Medium Priority Bugs

### 3. ⚠️ Version mismatch in help text
**Location**: `cli_v4.py`  
**Issue**: Help text says "Manus CLI v4.0" but version is 5.2.0  
**Impact**: Confusing for users  
**Fix**: Update help text to show correct version or make it dynamic

## Testing Status

- ✅ Installation works
- ✅ Version command works  
- ✅ Help command works
- ✅ Configure command works
- ❌ Chat command BROKEN (API method mismatch)
- ❌ Roles command BROKEN (wrong field access)
- ⏳ Task command NOT TESTED
- ⏳ History command NOT TESTED
- ⏳ Spec-Kit workflow NOT TESTED

## Next Steps

1. Fix critical bugs 1 & 2
2. Test all commands end-to-end
3. Test Spec-Kit workflow
4. Test v5.1 and v5.2 features via CLI
5. Create comprehensive test report
