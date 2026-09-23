import { type CollectionEntry, getCollection } from "astro:content";
import { getSortedPosts } from "../../../utils/getSortedPosts";
import { generateOgImageForPost } from "../../../utils/generateOgImages";

export async function getStaticPaths() {
  const posts = await getCollection("posts");
  const sortedPosts = getSortedPosts(posts);

  return sortedPosts.map((post: any) => ({
    params: { slug: post.id.replace(/\.(md|mdx)$/, "") },
    props: post,
  }));
}

export async function GET({ props }: { props: CollectionEntry<"posts"> }) {
  return new Response(await generateOgImageForPost(props), {
    headers: { "Content-Type": "image/png" },
  });
}
