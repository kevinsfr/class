-- CS 61A Fall 2014
-- Name:
-- Login:



select name from dogs where height > 24 and height <= 35;
-- Expected output:
--   abraham
--   eisenhower
--   fillmore
--   grover
--   herbert

-- All dogs with parents ordered by decreasing height of their parent
select child from parents, dogs where name=parent order by -height;
-- Expected output:
--   herbert
--   fillmore
--   abraham
--   delano
--   grover
--   barack
--   clinton

-- Sentences about siblings that are the same size
with
  siblings (first, second) as (
    select a.child as first, b.child as second
      from parents as a, parents as b
      where a.parent = b.parent and a.child < b.child
  )
select first || " and " || second || " are " || a.size || " siblings"
  from siblings, dog_size as a, dog_size as b
  where a.name = first and b.name = second and a.size = b.size;
-- Expected output:
--   barack and clinton are standard siblings
--   abraham and grover are toy siblings

-- Ways to stack 4 dogs to a height of at least 170, ordered by total height
with
  stacks(first, second, third, fourth, total_height) as (
    select a.name, b.name, c.name, d.name, a.height + b.height + c.height + d.height
      from dogs as a, dogs as b, dogs as c, dogs as d
      where a.height + b.height + c.height + d.height >= 170 and a.height < b.height and b.height < c.height and c.height < d.height
  )
select first || ", " || second || ", " || third || ", " || fourth, total_height
  from stacks order by total_height;
-- Expected output:
--   abraham, delano, clinton, barack|171
--   grover, delano, clinton, barack|173
--   herbert, delano, clinton, barack|176
--   fillmore, delano, clinton, barack|177
--   eisenhower, delano, clinton, barack|180

-- All non-parent relations ordered by height difference
select "REPLACE THIS LINE WITH YOUR SOLUTION";
-- Expected output:
--   fillmore|barack
--   eisenhower|barack
--   fillmore|clinton
--   eisenhower|clinton
--   eisenhower|delano
--   abraham|eisenhower
--   grover|eisenhower
--   herbert|eisenhower
--   herbert|fillmore
--   fillmore|herbert
--   eisenhower|herbert
--   eisenhower|grover
--   eisenhower|abraham
--   delano|eisenhower
--   clinton|eisenhower
--   clinton|fillmore
--   barack|eisenhower
--   barack|fillmore


