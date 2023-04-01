import { ref } from "vue";
import { defineStore } from "pinia";

/* Defining a store. */
export const useAppStore = defineStore("app", () => {
  /* Creating a reactive object. */
  const userID = ref("");
  const userName = ref("");
  const currentNotebookID = ref("");
  const currentPageID = ref("");
  return { userID, userName, currentNotebookID, currentPageID };
});
