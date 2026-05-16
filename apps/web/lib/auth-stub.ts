/**
 * Hardcoded current user for Phase 2 and 3. Replaced by NextAuth in Phase 4.
 *
 * Mirrors the seed user `player@zpots.ai` from `data/database.py:_seed`.
 */
export const currentUser = {
  id: 1,
  name: 'Alex Siriwan',
  email: 'player@zpots.ai',
};

/**
 * Hardcoded current owner for Phase 3a. Mirrors the seed user
 * `owner@zpots.ai` in `data/database.py:_seed`. Replaced by NextAuth in Phase 4.
 */
export const currentOwner = {
  id: 3,
  name: 'Venue Admin',
  email: 'owner@zpots.ai',
};
