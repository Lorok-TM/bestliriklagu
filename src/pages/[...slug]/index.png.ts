import { type CollectionEntry, getCollection } from "astro:content";
import { getSortedPosts } from "../../utils/getSortedPosts";
import { generateOgImageForPost } from "../../utils/generateOgImages";

export async function getStaticPaths() {
  const posts = await getCollection("posts");
  const sortedPosts = getSortedPosts(posts);

  // Ditambahi ': any' supoyo TypeScript anteng
  return sortedPosts.map((post: any) => ({
    // Rute generator diselarasno langsung neng root domain!
    params: { slug: post.id.replace(/\.(md|mdx)\$/, "") },
    props: post,
  }));
}

export async function GET({ props }: { props: CollectionEntry<"posts"> }) {
  // Nimbal fungsi generator satori nggo nggambar PNG-ne
  return new Response(await generateOgImageForPost(props), {
    headers: { "Content-Type": "image/png" },
  });
}
