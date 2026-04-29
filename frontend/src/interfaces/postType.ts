export interface Post {
  id: number;
  author: string;
  title: string;
  content: string;
  created_at: string;
  image: string | null;
  likes_count: number;
  comments_count: number;
  is_liked: boolean;
}
