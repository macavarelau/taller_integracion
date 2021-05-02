<template>
  <div class="dropdown">
    <input
      class="dropdown-input"
      v-model="inputValue"
      type="text"
      placeholder="Buscar..."
    />
    <div v-show="inputValue" class="dropdown-list">
      <div
        v-for="item in itemList"
        :key="item.name"
        class="dropdown-item"
        v-on:click="select(item.name)"
      >
        <span>{{ item.name }}</span>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "Search",
  data() {
    return {
      inputValue: "",
    };
  },
  props: {
    itemList: Array,
  },
  methods: {
    select(name) {
      this.$emit("select-char", name);
      this.inputValue = null;
    },
  },
  watch: {
    inputValue: function (search) {
      this.$emit("search-text", search);
    },
  },
};
</script>
<style scoped>
.dropdown {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}
.dropdown-input,
.dropdown-selected {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid transparent;
  background: #ffffff;
  line-height: 1.5em;
  outline: none;
  border-radius: 8px;
}
.dropdown-input:focus,
.dropdown-selected:hover {
  background: #fff;
  border-color: #e2e8f0;
}
.dropdown-input::placeholder {
  opacity: 0.7;
}
.dropdown-selected {
  font-weight: bold;
  cursor: pointer;
}
.dropdown-list {
  position: absolute;
  width: 100%;
  max-height: 500px;
  margin-top: 42px;
  overflow-y: auto;
  background: #f5f5f5;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
.dropdown-item {
  border-bottom: rgb(224, 224, 224) solid 1px;
  border-left: rgb(224, 224, 224) solid 1px;
  border-right: rgb(224, 224, 224) solid 1px;
  display: flex;
  width: 100%;
  cursor: pointer;
}
.dropdown-item img {
  object-fit: cover;
}
.dropdown-item:hover {
  background: #edf2f7;
}
.dropdown-item-flag {
  max-width: 24px;
  max-height: 18px;
  margin: auto 12px auto 0px;
}
</style>
