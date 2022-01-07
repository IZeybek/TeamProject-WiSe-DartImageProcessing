<template>
  <v-app id="inspire">
    <v-app-bar app color="white" flat>
      <v-spacer />
      <v-app-bar-title
        ><div style="width: 200px">Welcome to Dart!</div></v-app-bar-title
      >
      <v-spacer />
    </v-app-bar>

    <v-main class="grey lighten-3">
      <router-view></router-view>
      <v-container> </v-container>
    </v-main>
  </v-app>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
./components/Playfield.vue
