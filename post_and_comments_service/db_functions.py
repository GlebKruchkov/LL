from db_connector import DBConnection
from datetime import datetime
import uuid
from typing import List, Optional, Tuple, Dict, Any

conn = DBConnection()

def create_tables():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL,
                is_private BOOLEAN NOT NULL,
                tags TEXT[] NOT NULL,
                likes_count INTEGER DEFAULT 0
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS post_views (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL REFERENCES posts(id),
                user_id TEXT NOT NULL,
                viewed_at TIMESTAMP NOT NULL
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS post_likes (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL REFERENCES posts(id),
                user_id TEXT NOT NULL,
                liked_at TIMESTAMP NOT NULL,
                UNIQUE(post_id, user_id)
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                post_id TEXT NOT NULL REFERENCES posts(id),
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """)
        conn.commit()

def create_post(title: str, content: str, user_id: str, is_private: bool, tags: List[str]) -> str:
    post_id = str(uuid.uuid4())
    created_at = updated_at = datetime.now()
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO posts (id, title, content, user_id, created_at, updated_at, is_private, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (post_id, title, content, user_id, created_at, updated_at, is_private, tags))
        conn.commit()
    
    return post_id

def update_post(post_id: str, title: str, content: str, user_id: str, 
               is_private: bool, tags: List[str]) -> bool:
    updated_at = datetime.now()
    
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE posts
            SET title = %s, content = %s, updated_at = %s, is_private = %s, tags = %s
            WHERE id = %s AND user_id = %s
        """, (title, content, updated_at, is_private, tags, post_id, user_id))
        conn.commit()
        return cur.rowcount > 0

def delete_post(post_id: str, user_id: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM posts
            WHERE id = %s AND user_id = %s
        """, (post_id, user_id))
        conn.commit()
        return cur.rowcount > 0

def get_post(post_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, content, user_id, created_at, updated_at, is_private, tags
            FROM posts
            WHERE id = %s AND (NOT is_private OR user_id = %s)
        """, (post_id, user_id))
        post = cur.fetchone()
        if post:
            return {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "user_id": post[3],
                "created_at": post[4],
                "updated_at": post[5],
                "is_private": post[6],
                "tags": post[7]
            }
        return None

def list_posts(user_id: str, page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    offset = (page - 1) * per_page
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) FROM posts
            WHERE NOT is_private OR user_id = %s
        """, (user_id,))
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT id, title, content, user_id, created_at, updated_at, is_private, tags
            FROM posts
            WHERE NOT is_private OR user_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (user_id, per_page, offset))
        
        posts = []
        for post in cur.fetchall():
            posts.append({
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "user_id": post[3],
                "created_at": post[4],
                "updated_at": post[5],
                "is_private": post[6],
                "tags": post[7]
            })
    
    return posts, total

def track_post_view(post_id: str, user_id: str) -> str:
    view_id = str(uuid.uuid4())
    viewed_at = datetime.now()
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO post_views (id, post_id, user_id, viewed_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (view_id, post_id, user_id, viewed_at))
        conn.commit()
    
    return view_id

def like_post(post_id: str, user_id: str) -> bool:
    like_id = str(uuid.uuid4())
    liked_at = datetime.now()
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO post_likes (id, post_id, user_id, liked_at)
            VALUES (%s, %s, %s, %s)
        """, (like_id, post_id, user_id, liked_at))
        
        cur.execute("""
            UPDATE posts
            SET likes_count = likes_count + 1
            WHERE id = %s
        """, (post_id,))
        
        conn.commit()
        return True

def create_comment(post_id: str, user_id: str, content: str) -> str:
    comment_id = str(uuid.uuid4())
    created_at = updated_at = datetime.now()
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO comments (id, post_id, user_id, content, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (comment_id, post_id, user_id, content, created_at, updated_at))
        conn.commit()
    
    return comment_id

def list_comments(post_id: str, page: int, per_page: int) -> Tuple[List[Dict[str, Any]], int]:
    offset = (page - 1) * per_page
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*) FROM comments
            WHERE post_id = %s
        """, (post_id,))
        total = cur.fetchone()[0]

        cur.execute("""
            SELECT id, post_id, user_id, content, created_at, updated_at
            FROM comments
            WHERE post_id = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """, (post_id, per_page, offset))
        
        comments = []
        for comment in cur.fetchall():
            comments.append({
                "id": comment[0],
                "post_id": comment[1],
                "user_id": comment[2],
                "content": comment[3],
                "created_at": comment[4],
                "updated_at": comment[5]
            })
    
    return comments, total

def close_connection():
    conn.close()
