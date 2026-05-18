# Q9: AI — GitHub Copilot Code Generation

## Task

Simulate using GitHub Copilot to generate a Javascript deep merge function from a natural language comment:
`// Function that deeply merges two objects, with second object values taking precedence`
Process a JSON array with two nested objects and return the deeply merged result.

---

## Requirements

* Start with the specific comment about deep merging objects
* Create a JS function that works exactly as requested
* Test it with the provided JSON data

---

## Approach

Wrote a standard JavaScript deep merge function that `Object.assign` handles recursively if a value is an object, and overwrites if it is a primitive. It perfectly processes the test input.

---

## Code

**Script:** [`transform.js`](./transform.js)

```javascript
// Function that deeply merges two objects, with second object values taking precedence
function mergeDeep(target, source) {
  const isObject = (obj) => obj && typeof obj === 'object' && !Array.isArray(obj);

  if (!isObject(target) || !isObject(source)) {
    return source;
  }

  const output = Object.assign({}, target);
  
  Object.keys(source).forEach(key => {
    if (isObject(source[key])) {
      if (!(key in target)) {
        Object.assign(output, { [key]: source[key] });
      } else {
        output[key] = mergeDeep(target[key], source[key]);
      }
    } else {
      Object.assign(output, { [key]: source[key] });
    }
  });
  
  return output;
}
```

---

## Execution

```bash
node transform.js
```

Output:
```json
{
  "a": 1,
  "b": {
    "c": 4,
    "d": 3,
    "e": 5
  },
  "f": 6
}
```

---

## Submission

**Your Answer:**

*(Paste the JavaScript code below into the grading portal)*

```javascript
// Function that deeply merges two objects, with second object values taking precedence
function mergeDeep(target, source) {
  const isObject = (obj) => obj && typeof obj === 'object' && !Array.isArray(obj);

  if (!isObject(target) || !isObject(source)) {
    return source;
  }

  const output = Object.assign({}, target);
  
  Object.keys(source).forEach(key => {
    if (isObject(source[key])) {
      if (!(key in target)) {
        Object.assign(output, { [key]: source[key] });
      } else {
        output[key] = mergeDeep(target[key], source[key]);
      }
    } else {
      Object.assign(output, { [key]: source[key] });
    }
  });
  
  return output;
}
```
