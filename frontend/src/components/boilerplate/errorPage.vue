<template>
  <v-app>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <div class="text-md-center">
          <h1>{{ errorCode }}</h1>
          <h3 class="my-3 headline ">{{ errorMessage }}</h3>
        </div>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: 'errorPage',
  data: () => ({}),
  computed: {
    errorCode() {
      try {
        return this.$route.params.errorCode;
      } catch (error) {
        return 'Authentification Error';
      }
    },
    errorMessage() {
      try {
        return this.$route.params.errorMessage;
      } catch (error) {
        return '';
      }
    },
  },
  async created() {
    try {
      // if okta token exists
      await this.$auth.logout();
    } catch (error) {
      // do nothing if there is no okta token
    }
  },
};
</script>
<style scoped lang="css">
h1 {
  font-size: 70px;
  line-height: 150px;
  font-weight: 700;
  color: #252932;
  text-shadow: rgba(61, 61, 61, 0.3) 1px 1px, rgba(61, 61, 61, 0.2) 2px 2px, rgba(61, 61, 61, 0.3) 3px 3px;
}
</style>
