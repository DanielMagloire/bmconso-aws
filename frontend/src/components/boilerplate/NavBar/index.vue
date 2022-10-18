<template>
  <div>
    <v-app-bar :clipped-left="$vuetify.breakpoint.lgAndUp" color="#949494" dark app elevation="1" height="56" fixed class="nav-main">
      <v-avatar tile width="90px">
        <v-img :src="require(`@/assets/ENGIE_Solutions2.png`)" alt="Engie Cofely"> </v-img>
      </v-avatar>
      <!-- NavBar Buttons -->
      <v-flex class="router-link-wrap">
        <router-link to="/profil" class="inset-text config" id="link-first">profil</router-link>
        <router-link to="/configuration" class="inset-text config" id="link-first">configuration</router-link>
        <router-link to="/previsions" class="inset-text prev" id="link-second">prévisions</router-link>
        <router-link to="/historique" class="inset-text config" id="link-first">historique</router-link>
      </v-flex>
      <!-- Rigth menu for small screen-->
      <v-menu
        offset-y
        origin="center center"
        :nudge-bottom="10"
        transition="slide-y-transition"
        :min-width="180"
        v-if="$vuetify.breakpoint.xs"
      >
        <v-btn icon>
          <v-icon>more_vert</v-icon>
        </v-btn>
        <c-setting-list></c-setting-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  name: 'c-toolbar',
};
</script>
<style scoped>
.router-link-wrap {
  display: flex;
}
.v-application a {
  flex-grow: 2;
  color: white;
  text-decoration: none;
  text-transform: uppercase;
  font-size: 200%;
  font-weight: 800;
  text-align: center;
  line-height: 56px;
}
a:hover {
  color: #71d0ff;
}
a.router-link-active {
  color: white;
  background-color: #00aaff;
  height: 56px;
}
</style>
