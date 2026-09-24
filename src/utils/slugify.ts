import { slugify as utilSlugify } from "transliteration";

// Iki fungsi kanggo nggawe link URL tetep huruf cilik lan aman (slug)
export const slugifyStr = (str: string) => utilSlugify(str);

export const slugify = (tags: string[]) => {
  return tags.map(tag => ({
    name: tag, // Iki jeneng asli sing bakal dadi teks anchor
    slug: utilSlugify(tag), // Iki sing dadi link URL (tetep huruf cilik)
  }));
};

// Fungsi tambahan kanggo nggawe teks dadi Huruf Gedhe ing awal kata (Title Case)
export const capitalizeTag = (tag: string) => {
  return tag
    .split(" ")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
};

export default slugify;
