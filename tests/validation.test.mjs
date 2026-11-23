import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validatePilot, manilaToday, MESSAGES } from '../lib/pilot.ts';
const valid = { pilotName: 'Ace', age: '25', email: 'a@b.com', mobile: '09171234567' };
const cases = [
 ['blank name', { pilotName: '' }, 'pilotName', MESSAGES.pilotName],
 ['age 17', { age: '17' }, 'age', MESSAGES.age],
 ['age 61', { age: '61' }, 'age', MESSAGES.age],
 ['invalid email', { email: 'banana' }, 'email', MESSAGES.email],
 ['blank mobile', { mobile: '' }, 'mobile', MESSAGES.mobile],
 ['blank age', { age: '' }, 'age', MESSAGES.ageRequired],
 ['long name', { pilotName: 'Captain Zoomzoom Starfighter' }, 'pilotName', MESSAGES.pilotName],
];
for (const [name, patch, field, message] of cases) test(name, () => { const result = validatePilot({ ...valid, ...patch }); assert.equal(result.ok, false); assert.equal(result.errors[field], message); });
test('Nova success', () => { assert.equal(validatePilot({ ...valid, pilotName: 'Nova', age: '30', email: 'nova@academy.edu' }).ok, true); });
for (const age of ['18','60']) test('inclusive age ' + age, () => assert.equal(validatePilot({ ...valid, age }).ok, true));
for (const age of ['5','25.5','25abc','-25','1e2']) test('invalid integer ' + age, () => assert.equal(validatePilot({ ...valid, age }).ok, false));
test('call sign endpoints', () => { for (const name of ['Ace','A'.repeat(20)]) assert.equal(validatePilot({ ...valid, pilotName: name }).ok, true); assert.equal(validatePilot({ ...valid, pilotName: 'AB' }).ok, false); });
test('mobile length and syntax', () => { for (const mobile of ['091712345678','abc','000','---']) assert.equal(validatePilot({ ...valid, mobile }).ok, false); });
test('non-object bodies and wrong types', () => { for(const raw of [null, [], 'hello', { pilotName: 999, age: true }]) assert.equal(validatePilot(raw).ok, false); });
test('launch yesterday, today, future and invalid calendar date', () => { assert.equal(validatePilot({ ...valid, launchDate: '2026-11-22' },'2026-11-23').errors.launchDate, MESSAGES.launchDate); for (const date of ['2026-11-23','2026-11-24']) assert.equal(validatePilot({ ...valid, launchDate: date },'2026-11-23').ok,true); assert.equal(validatePilot({ ...valid, launchDate: '2026-02-30' },'2026-01-01').ok,false); });
test('Manila date crosses UTC boundary', () => assert.equal(manilaToday(new Date('2026-11-22T17:00:00Z')),'2026-11-23'));
