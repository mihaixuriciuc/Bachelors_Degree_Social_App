import { Post } from "../../interfaces/postType";
import "./PostsGrid.scss";

interface PostsGridProps {
  posts: Post[];
  onPostClick: (post: Post) => void;
}

function PostsGrid({ posts, onPostClick }: PostsGridProps) {
  if (posts.length === 0) {
    return <p className="no-posts">No posts yet.</p>;
  }

  return (
    <main className="posts-grid">
      {posts.map((post) => (
        <div
          key={post.id}
          className="grid-item"
          onClick={() => onPostClick(post)}
        >
          {post.image ? (
            <img src={post.image} alt={post.title} />
          ) : (
            <div className="text-only-post">
              <p>{post.title}</p>
            </div>
          )}
        </div>
      ))}
    </main>
  );
}

export default PostsGrid;
