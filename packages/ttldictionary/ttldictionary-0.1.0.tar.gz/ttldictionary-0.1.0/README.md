# TTL-Dictionary

A basic yet useful module made to streamline projects that need a basic TTL system that also is compatible with most serializers.

```python
ttl_dict = TTLDict()
ttl_dict.set('a', 1, ttl=5)  # Key 'a' will expire in 5 seconds
print(ttl_dict.get('a'))  # Output: 1
time.sleep(6)
print(ttl_dict.get('a'))  # Output: None (expired)

# Serialize to JSON
ttl_dict.set('b', 2, ttl=10)
json_data = json.dumps(ttl_dict)  # Output: {"b": 2}
```