/**
 * Business function unit test example.
 */
import addition from '@/business/count/addition';

describe('[business/count/addition tests]', () => {
  it('should add values', () => {
    expect(addition(17, 25)).toBe(42);
  });
});
