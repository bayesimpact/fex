# Manual tests

TODO: Automate all of these tests.

Before each release, make sure that all of the following scenarios still work.

## Runner

Test the deployment mode of the runner. You can use `examples/simple_example.py --deploy` to perform the following tests.

* If you run the above command:
  - outside of a git repository, the program should exit with an error message.
  - in a git repository that does not have a remote set, the program should exit with an error message.
  - in a git repository that has uncommitted changes, it should exit with an error message.
