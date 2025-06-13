const calculerPointsFidelite = require('./fidelite');

test('Client non VIP', () => {
  expect(calculerPointsFidelite(45, false)).toBe(4);
  expect(calculerPointsFidelite(5, false)).toBe(0);
});

test('Client VIP', () => {
  expect(calculerPointsFidelite(45, true)).toBe(8);
  expect(calculerPointsFidelite(9.99, true)).toBe(0);
});
