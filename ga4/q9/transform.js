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

// Test Data
const data = [
    {
        "a": 1,
        "b": {
            "c": 2,
            "d": 3
        }
    },
    {
        "b": {
            "c": 4,
            "e": 5
        },
        "f": 6
    }
];

// Test the function with the provided data
const result = mergeDeep(data[0], data[1]);
console.log(JSON.stringify(result, null, 2));
