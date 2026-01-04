<script setup>
import navItems from '@/navigation/vertical'
import { useSubscriptionStore } from '@/stores/subscription'
import { themeConfig } from '@themeConfig'

// Components
import Footer from '@/layouts/components/Footer.vue'
import NavbarThemeSwitcher from '@/layouts/components/NavbarThemeSwitcher.vue'
import UserProfile from '@/layouts/components/UserProfile.vue'
import RoleSwitcher from '@/components/RoleSwitcher.vue'
import NavBarI18n from '@core/components/I18n.vue'

// @layouts plugin
import { VerticalNavLayout } from '@layouts'

// Subscription store for role-based navigation
const subscriptionStore = useSubscriptionStore()

// Filter navigation items based on user role
const filteredNavItems = computed(() => {
  return navItems.filter(item => {
    // Hide admin items from non-admin users
    if (item.meta?.requiresAdmin && !subscriptionStore.isSuperAdmin) {
      return false
    }
    return true
  })
})

// SECTION: Loading Indicator
const isFallbackStateActive = ref(false)
const refLoadingIndicator = ref(null)

const router = useRouter()
const route = useRoute()

// Horizontal menu items matching NeoTrader design
const horizontalMenuItems = ref([
  { title: 'Stock Analyser', icon: 'tabler-chart-line', route: '/stock-analyser' },
  { title: 'Changed Now', icon: 'tabler-refresh', route: '/changed-now' },
  { title: 'Rolling Ticker', icon: 'tabler-mail', route: '/rolling-ticker' },
  { title: 'Ask Help', icon: 'tabler-help-circle', route: '/ask-help' },
  { title: 'Connect Your Broker', icon: 'tabler-building-bank', route: '/connect-broker' },
])

const navigateTo = (path) => {
  router.push(path)
}

watch([
  isFallbackStateActive,
  refLoadingIndicator,
], () => {
  if (isFallbackStateActive.value && refLoadingIndicator.value)
    refLoadingIndicator.value.fallbackHandle()
  if (!isFallbackStateActive.value && refLoadingIndicator.value)
    refLoadingIndicator.value.resolveHandle()
}, { immediate: true })
// !SECTION
</script>

<template>
  <VerticalNavLayout :nav-items="filteredNavItems">
    <!-- 👉 navbar -->
    <template #navbar="{ toggleVerticalOverlayNavActive }">
      <div class="d-flex h-100 align-center w-100">
        <IconBtn
          id="vertical-nav-toggle-btn"
          class="ms-n3 d-lg-none"
          @click="toggleVerticalOverlayNavActive(true)"
        >
          <VIcon
            size="26"
            icon="tabler-menu-2"
          />
        </IconBtn>

        <!-- Horizontal Menu Items - NeoTrader Style -->
        <div class="d-none d-md-flex align-center gap-4 ms-4 horizontal-nav-menu">
          <a
            v-for="item in horizontalMenuItems"
            :key="item.title"
            :class="['horizontal-nav-item', { 'active': route.path === item.route }]"
            @click="navigateTo(item.route)"
          >
            <VIcon :icon="item.icon" size="22" class="me-2" />
            <span class="nav-item-text">{{ item.title }}</span>
          </a>
        </div>

        <VSpacer />

        <RoleSwitcher class="me-2" />
        <NavbarThemeSwitcher />

        <NavBarI18n
          v-if="themeConfig.app.i18n.enable && themeConfig.app.i18n.langConfig?.length"
          :languages="themeConfig.app.i18n.langConfig"
        />
        <UserProfile />
      </div>
    </template>

    <AppLoadingIndicator ref="refLoadingIndicator" />

    <!-- 👉 Pages -->
    <RouterView v-slot="{ Component }">
      <Suspense
        :timeout="0"
        @fallback="isFallbackStateActive = true"
        @resolve="isFallbackStateActive = false"
      >
        <Component :is="Component" />
      </Suspense>
    </RouterView>

    <!-- 👉 Footer -->
    <template #footer>
      <Footer />
    </template>

    <!-- 👉 Customizer -->
    <!-- <TheCustomizer /> -->
  </VerticalNavLayout>
</template>

<style lang="scss" scoped>
.horizontal-nav-menu {
  .horizontal-nav-item {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    color: rgba(var(--v-theme-on-surface), 0.78);
    font-size: 14px;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s ease;
    white-space: nowrap;

    &:hover {
      color: rgb(var(--v-global-theme-primary));
      background-color: rgba(var(--v-global-theme-primary), 0.08);
    }

    &.active {
      color: rgb(var(--v-global-theme-primary));
      background-color: rgba(var(--v-global-theme-primary), 0.12);
    }

    .nav-item-text {
      letter-spacing: 0.25px;
    }
  }
}
</style>
