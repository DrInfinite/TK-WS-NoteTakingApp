import { createRouter, createWebHistory } from "vue-router";
import { useAppStore } from "../stores/appStore";
import EditNotebookVue from "../views/EditNotebook.vue";
import HomeVue from "../views/Home.vue";
import NotFoundVue from "../views/NotFound.vue";
import SignInPageVue from "../views/SignInPage.vue";
import SignUpPageVue from "../views/SignUpPage.vue";
import { storeToRefs } from "pinia";

/* Creating a router object. */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: SignInPageVue,
      meta: { requiresAuth: false, transition: "slide-left" },
    },
    {
      path: "/signup",
      component: SignUpPageVue,
      meta: { requiresAuth: false },
    },
    {
      path: "/home",
      component: HomeVue,
      meta: { requiresAuth: true },
    },
    {
      path: "/home/:notebook_id",
      component: EditNotebookVue,
      meta: { requiresAuth: true },
    },
    {
      path: "/:pathMatch(.*)",
      component: NotFoundVue,
    },
  ],
});

/* Checking if the user is logged in. If not, it redirects to the login page. */
router.beforeEach(async (to) => {
  const store = useAppStore();
  const { userID } = storeToRefs(store);
  console.log(userID.value);
  if (to.meta.requiresAuth && userID.value == "") {
    router.replace("/");
  }
});

export default router;
