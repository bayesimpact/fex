# Manual tests

TODO: Automate all of these tests.

Before each release, make sure that all of the following scenarios still work.

## Runner

Test the deployment mode of the runner. You can use `examples/simple_example.py --deploy` to perform the following tests. The following instructions assume that you are in the fex repository at the beginning of each test.

Test that the runner exits with an error when run in deployment mode within a folder that is not a git repository.

```
cd ..
fex/examples/simple_example.py --deploy
cd fex
```

Test that the runner exits with an error if your are in a git repository with no remote set.

```
cd ..
mkdir test_repo
cd test_repo
git init
touch test.bla
git add test.bla
git commit -m 'first commit'
../fex/examples/simple_example.py --deploy
cd ..
rm -rf test_repo
cd fex
```

Test that the runner exits with an error if the git repository has uncommitted changes.

```
cd ..
mkdir test_repo
cd test_repo
git init
touch test.bla
../fex/examples/simple_example.py --deploy
cd ..
rm -rf test_repo
cd fex
```
