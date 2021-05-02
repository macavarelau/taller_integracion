<template>
  <b-navbar>
    <template #start>
      <b-navbar-item href="#"> Tarea 1 - Taller de Integración </b-navbar-item>
    </template>

    <template #end>
      <b-navbar-item tag="div">
        <Search
          @search-text="search"
          @select-char="select"
          :itemList="searchList"
        />
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
import Search from "../components/Search.vue";
export default {
  name: "Navbar",
  components: {
    Search,
  },
  data() {
    return {
      searched: "",
    };
  },
  props: {
    searchList: Array,
  },
  methods: {
    search(char) {
      this.$emit("search-text", char);
    },
    select(name) {
      this.$emit("select-char", name);
    },
  },
};
</script>
<style scoped>
.navbar {
  font-family: "Noto Sans JP", sans-serif, bold;
  background-color: #ededed;
  color: white;
}
.navbar-item:hover {
  color: #4a4a4a !important;
}
.navbar-item:focus {
  color: #4a4a4a !important;
}
.navbar-item:focus-within {
  color: #4a4a4a !important;
}
</style>
