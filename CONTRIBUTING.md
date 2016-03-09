# How to contribute to jss-recipes

1. Sign in with your GitHub.com account, if you're not already.

2. Click the __Fork__ button above.

    ![Fork button](img/fork-button.png)

3. In your new copy of the repo, make whatever changes or additions you like. Commit your changes with descriptive commit messages.

4. If you create or modify recipes, make sure to use the included validator to make sure the recipe matches the expected behavior of jss-recipes:

    ```
    $ ./validate_recipes.py Atom/*.recipe
    --------------------------------------
     Testing recipe: Atom/Atom.jss.recipe
    --------------------------------------
    OK
    ```

5. Once you're all done, submit a pull request back to our jss-recipes repo.

    ![Pull request](img/pull-request.png)

    One of the repo's owners will review your changes (usually within a day or two) and respond accordingly.

Thanks for contributing!
