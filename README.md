# Book Recommender

An information filtering system that seeks to predict the future preference of a set of books for a user, and recommend the top books based on predicted ratings.

This dataset contains six million ratings for ten thousand most popular (with most ratings) books. There are also:

* books marked to read by the users
* book metadata (author, year, etc.) 
* tags/shelves/genres

## Access

Some of these files are quite large, so GitHub won't show their contents online. See [samples/](samples/) for smaller CSV snippets.

Open the [notebook](quick_look.ipynb) for a quick look at the data. Download individual zipped files from [releases](https://github.com/zygmuntz/goodbooks-10k/releases).

## Dataset Content
* **Ratings.csv** contains ratings sorted by time.
* **to_read.csv** provides IDs of the books marked "to read" by each user, as _user_id,book_id_ pairs, sorted by time.
* **books.csv** has metadata for each book (goodreads IDs, authors, title, average rating, etc.).
You can use the goodreads book and work IDs to create URLs as follows:

    https://www.goodreads.com/book/show/2767052   
    https://www.goodreads.com/work/editions/2792775 
* **book_tags.csv** contains tags/shelves/genres assigned by users to books.

## Architecture
We used matrix factorization technique to extract latent factors from user ratings matrix and trained the model using **Stochastic Gradient Descent (SGD)**.

Firstly, we randomly intialized the latent vectors (Along with biases) of users and books of dimensions (NumUser,30) and (30,NumBooks) respectively. After hypertuning we came to use learning rate of 0.001 and regularization parameter of 0.01 .

## Accuracy
After training for 100 epochs, we obtained RMSE of 0.037 on training set and 0.04 on test set.


