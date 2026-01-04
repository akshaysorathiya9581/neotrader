<script setup>
import { useSubscriptionStore } from '@/stores/subscription'

const store = useSubscriptionStore()

const currentRole = computed({
  get: () => store.currentUser.role,
  set: (val) => store.setUserRole(val)
})

const roles = [
  { title: 'Normal User', value: 'user' },
  { title: 'SuperAdmin', value: 'superadmin' },
]
</script>

<template>
  <div class="role-switcher">
    <VMenu>
      <template #activator="{ props }">
        <VBtn 
          v-bind="props" 
          :color="currentRole === 'superadmin' ? 'error' : 'primary'" 
          variant="tonal"
          size="small"
        >
          <VIcon :icon="currentRole === 'superadmin' ? 'tabler-shield-check' : 'tabler-user'" class="me-1" />
          {{ currentRole === 'superadmin' ? 'SuperAdmin' : 'User' }}
          <VIcon icon="tabler-chevron-down" class="ms-1" />
        </VBtn>
      </template>
      <VList density="compact">
        <VListSubheader>Switch Role (Demo)</VListSubheader>
        <VListItem 
          v-for="role in roles" 
          :key="role.value" 
          :active="currentRole === role.value"
          @click="currentRole = role.value"
        >
          <template #prepend>
            <VIcon :icon="role.value === 'superadmin' ? 'tabler-shield-check' : 'tabler-user'" />
          </template>
          <VListItemTitle>{{ role.title }}</VListItemTitle>
        </VListItem>
        <VDivider class="my-1" />
        <VListItem v-if="currentRole !== 'superadmin'" to="/subscription">
          <template #prepend>
            <VIcon icon="tabler-credit-card" />
          </template>
          <VListItemTitle>View Plans</VListItemTitle>
        </VListItem>
        <VListItem v-else to="/admin">
          <template #prepend>
            <VIcon icon="tabler-settings" />
          </template>
          <VListItemTitle>Admin Dashboard</VListItemTitle>
        </VListItem>
      </VList>
    </VMenu>
    
    <!-- Current Plan Badge -->
    <VChip v-if="store.currentPlan && currentRole !== 'superadmin'" :color="store.currentPlan.color" size="small" class="ms-2">
      {{ store.currentPlan.name }} Plan
    </VChip>
  </div>
</template>

<style scoped>
.role-switcher {
  display: flex;
  align-items: center;
}
</style>
