/**
 * Unit tests for getUserById (Bug API-404 fix)
 *
 * FIRST compliance:
 *   F - Fast: no I/O, all tests run in-memory
 *   I - Independent: each test creates fresh req/res mocks via beforeEach
 *   R - Repeatable: no Date.now(), Math.random(), or external calls
 *   S - Self-validating: every test has explicit expect assertions
 *   T - Timely: tests written for the changed code only (getUserById)
 */

const { getUserById, getAllUsers } = require('../demo-bug-fix/src/controllers/userController');

// Helper to create mock Express req/res objects
function mockReqRes(id) {
  const req = { params: { id } };
  const res = {
    json: jest.fn(),
    status: jest.fn().mockReturnThis(),
  };
  return { req, res };
}

describe('getUserById — Bug API-404 fix (type coercion)', () => {
  // --- Happy path ---

  it('returns user when id is passed as numeric string "123"', async () => {
    const { req, res } = mockReqRes('123');

    await getUserById(req, res);

    expect(res.json).toHaveBeenCalledWith({
      id: 123,
      name: 'Alice Smith',
      email: 'alice@example.com',
    });
    expect(res.status).not.toHaveBeenCalled();
  });

  it('returns user when id is "456"', async () => {
    const { req, res } = mockReqRes('456');

    await getUserById(req, res);

    expect(res.json).toHaveBeenCalledWith({
      id: 456,
      name: 'Bob Johnson',
      email: 'bob@example.com',
    });
  });

  it('returns user when id is "789"', async () => {
    const { req, res } = mockReqRes('789');

    await getUserById(req, res);

    expect(res.json).toHaveBeenCalledWith({
      id: 789,
      name: 'Charlie Brown',
      email: 'charlie@example.com',
    });
  });

  // --- Bug regression: the exact scenario that was broken ---

  it('REGRESSION: strict equality "123" === 123 would have failed — parseInt fixes it', async () => {
    // Before fix: users.find(u => u.id === "123") → always false → 404
    // After fix:  users.find(u => u.id === parseInt("123", 10)) → 123 === 123 → true → 200
    const { req, res } = mockReqRes('123');

    await getUserById(req, res);

    // Must NOT call 404
    expect(res.status).not.toHaveBeenCalledWith(404);
    // Must call json with the user
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ id: 123 }));
  });

  // --- 404 error path ---

  it('returns 404 when user id does not exist', async () => {
    const { req, res } = mockReqRes('999');

    await getUserById(req, res);

    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({ error: 'User not found' });
  });

  // --- Edge cases ---

  it('returns 404 for non-numeric id "abc" (parseInt returns NaN)', async () => {
    const { req, res } = mockReqRes('abc');

    await getUserById(req, res);

    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({ error: 'User not found' });
  });

  it('returns 404 for id "0" (no user with id 0)', async () => {
    const { req, res } = mockReqRes('0');

    await getUserById(req, res);

    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({ error: 'User not found' });
  });

  it('returns 404 for negative id "-1"', async () => {
    const { req, res } = mockReqRes('-1');

    await getUserById(req, res);

    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({ error: 'User not found' });
  });

  it('returns 404 for empty string id ""', async () => {
    const { req, res } = mockReqRes('');

    await getUserById(req, res);

    expect(res.status).toHaveBeenCalledWith(404);
    expect(res.json).toHaveBeenCalledWith({ error: 'User not found' });
  });
});

describe('getAllUsers — unchanged, smoke test', () => {
  it('returns all 3 users', async () => {
    const { req, res } = mockReqRes(null);

    await getAllUsers(req, res);

    const result = res.json.mock.calls[0][0];
    expect(Array.isArray(result)).toBe(true);
    expect(result).toHaveLength(3);
  });
});
