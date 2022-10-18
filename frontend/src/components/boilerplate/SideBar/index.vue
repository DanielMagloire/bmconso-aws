<template>
  <v-navigation-drawer id="appDrawer" :clipped="true" v-model="isCollapse" fixed :width="285" app>
    <!-- small & medium screen sidebar -->
    <v-list dense expand>
      <template v-for="(item, i) in routes">
        <!--group with subitems-->
        <v-list-group v-if="item.children" :key="i" :group="item.meta.group" :prepend-icon="item.meta.icon" no-action="no-action">
          <v-list-item slot="activator" ripple="ripple">
            <v-list-item-content>
              <v-list-item-title>{{ generateRouteTitle(item.meta.title) }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <template v-for="(subItem, j) in item.children">
            <!--sub group-->
            <v-list-group v-if="subItem.children" :key="j" :group="subItem.meta.group" no-action="no-action">
              <v-list-item slot="activator" ripple="ripple">
                <v-list-item-action>
                  <v-icon>{{ subItem.meta.icon }}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>{{ generateRouteTitle(subItem.meta.title) }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-for="(subSubItem, k) in subItem.children" :key="k" :to="{ name: subSubItem.name }" ripple="ripple">
                <v-list-item-action>
                  <v-icon>{{ subSubItem.meta.icon }}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title>{{ generateRouteTitle(subSubItem.meta.title) }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-group>
            <!--child item-->
            <v-list-item v-else :key="j" :to="{ name: subItem.name }" ripple="ripple">
              <v-list-item-action>
                <v-icon>{{ subItem.meta.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>
                  <span>{{ generateRouteTitle(subItem.meta.title) }}</span>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list-group>
        <!--List headers-->
        <v-subheader v-else-if="item.header" :key="i">{{ item.header }}</v-subheader>
        <!--List divider-->
        <v-divider v-else-if="item.divider" :key="i"></v-divider>
        <!--top-level link-->
        <v-list-item v-else :to="{ name: item.name }" ripple="ripple" :key="i">
          <v-list-item-action>
            <v-icon>{{ item.meta.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ generateRouteTitle(item.meta.title) }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { mapGetters } from 'vuex';
import { generateRouteTitle } from '@/utils/i18n';

export default {
  name: 'c-navigation-drawer',
  /* components: {
    VuePerfectScrollbar,
  }, */
  data: () => ({}),
  computed: {
    routes() {
      const routes = this.$router.options.routes.find(
        // eslint-disable-next-line
        (element) => element.name === 'Root'
      );
      const sideBarElement = routes.children.filter((element) => !element.meta.isHidden);
      return sideBarElement;
    },
    ...mapGetters({ sidebar: 'boilerplate/sidebar' }),
    isCollapse: {
      get() {
        return this.sidebar.opened;
      },
      set(val) {
        this.$store.dispatch('boilerplate/setSideBarOpened', val);
      },
    },
  },
  methods: {
    genChildTarget(item, subItem) {
      if (subItem.component) {
        return { name: subItem.component };
      }
      return `${item.group}/${subItem.name}`;
    },
    generateRouteTitle,
  },
};
</script>

<style lang="stylus">
#appDrawer {
  overflow: hidden;

  .drawer-menu--scroll {
    height: calc(100vh - 48px);
    overflow: auto;
  }
}
</style>
