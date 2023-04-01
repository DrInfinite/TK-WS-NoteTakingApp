import type Page from "./page.model";

/* Exporting the interface Notebook. */
export default interface Notebook {
  id: string;
  title: string;
  pages: Page[];
}
