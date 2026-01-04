<script setup>
import { useSubscriptionStore } from '@/stores/subscription'

const store = useSubscriptionStore()

// Stats
const totalModules = computed(() => store.modules.length)
const totalPlans = computed(() => store.plans.length)
const totalRevenue = computed(() => {
  // Simulated revenue
  return store.plans.reduce((acc, p) => acc + (p.price * Math.floor(Math.random() * 50 + 10)), 0)
})

// Recent activity (simulated)
const recentActivity = ref([
  { user: 'Rahul Sharma', action: 'Subscribed to Professional Plan', time: '2 mins ago', type: 'subscription' },
  { user: 'Priya Patel', action: 'Upgraded to Enterprise Plan', time: '15 mins ago', type: 'upgrade' },
  { user: 'Amit Kumar', action: 'Subscribed to Basic Plan', time: '1 hour ago', type: 'subscription' },
  { user: 'Sneha Gupta', action: 'Renewed Professional Plan', time: '2 hours ago', type: 'renewal' },
  { user: 'Vikram Singh', action: 'Subscribed to Enterprise Plan', time: '3 hours ago', type: 'subscription' },
])

// Plan distribution (simulated)
const planDistribution = ref([
  { plan: 'Basic', count: 145, color: 'info' },
  { plan: 'Professional', count: 287, color: 'success' },
  { plan: 'Enterprise', count: 68, color: 'warning' },
])

const totalUsers = computed(() => planDistribution.value.reduce((acc, p) => acc + p.count, 0))
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="error" variant="flat" size="small">SuperAdmin Dashboard</VChip>
          <VIcon icon="tabler-shield-check" size="18" color="error" />
          <span class="text-error text-caption">Admin Control Panel</span>
        </div>
        <div class="d-flex gap-2">
          <VBtn color="primary" size="small" to="/admin/plans">
            <VIcon icon="tabler-package" size="18" class="me-1" />
            Manage Plans
          </VBtn>
          <VBtn color="success" size="small" to="/admin/modules">
            <VIcon icon="tabler-puzzle" size="18" class="me-1" />
            Manage Modules
          </VBtn>
        </div>
      </VCardText>
    </VCard>

    <!-- Stats Cards -->
    <VRow class="mb-4">
      <VCol cols="12" md="3">
        <VCard>
          <VCardText class="d-flex align-center gap-4">
            <VAvatar color="primary" variant="tonal" size="48">
              <VIcon icon="tabler-puzzle" size="28" />
            </VAvatar>
            <div>
              <p class="text-caption text-medium-emphasis mb-0">Total Modules</p>
              <h4 class="text-h4">{{ totalModules }}</h4>
            </div>
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="3">
        <VCard>
          <VCardText class="d-flex align-center gap-4">
            <VAvatar color="success" variant="tonal" size="48">
              <VIcon icon="tabler-package" size="28" />
            </VAvatar>
            <div>
              <p class="text-caption text-medium-emphasis mb-0">Subscription Plans</p>
              <h4 class="text-h4">{{ totalPlans }}</h4>
            </div>
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="3">
        <VCard>
          <VCardText class="d-flex align-center gap-4">
            <VAvatar color="warning" variant="tonal" size="48">
              <VIcon icon="tabler-users" size="28" />
            </VAvatar>
            <div>
              <p class="text-caption text-medium-emphasis mb-0">Total Subscribers</p>
              <h4 class="text-h4">{{ totalUsers }}</h4>
            </div>
          </VCardText>
        </VCard>
      </VCol>
      <VCol cols="12" md="3">
        <VCard>
          <VCardText class="d-flex align-center gap-4">
            <VAvatar color="info" variant="tonal" size="48">
              <VIcon icon="tabler-currency-rupee" size="28" />
            </VAvatar>
            <div>
              <p class="text-caption text-medium-emphasis mb-0">Monthly Revenue</p>
              <h4 class="text-h4">₹{{ (totalRevenue / 1000).toFixed(0) }}K</h4>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <VRow>
      <!-- Plan Distribution -->
      <VCol cols="12" md="4">
        <VCard>
          <VCardTitle class="py-3">Plan Distribution</VCardTitle>
          <VCardText>
            <div v-for="item in planDistribution" :key="item.plan" class="mb-4">
              <div class="d-flex justify-space-between mb-1">
                <span class="text-body-2">{{ item.plan }}</span>
                <span class="text-body-2 font-weight-medium">{{ item.count }} users</span>
              </div>
              <VProgressLinear
                :model-value="(item.count / totalUsers) * 100"
                :color="item.color"
                height="8"
                rounded
              />
            </div>
          </VCardText>
        </VCard>
      </VCol>

      <!-- Recent Activity -->
      <VCol cols="12" md="8">
        <VCard>
          <VCardTitle class="py-3">Recent Activity</VCardTitle>
          <VTable density="compact">
            <thead>
              <tr>
                <th>User</th>
                <th>Action</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(activity, index) in recentActivity" :key="index">
                <td class="font-weight-medium">{{ activity.user }}</td>
                <td>
                  <VChip
                    :color="activity.type === 'upgrade' ? 'success' : activity.type === 'renewal' ? 'info' : 'primary'"
                    size="small"
                    variant="tonal"
                  >
                    {{ activity.action }}
                  </VChip>
                </td>
                <td class="text-medium-emphasis">{{ activity.time }}</td>
              </tr>
            </tbody>
          </VTable>
        </VCard>
      </VCol>
    </VRow>

    <!-- Quick Actions -->
    <VCard class="mt-4">
      <VCardTitle class="py-3">Quick Actions</VCardTitle>
      <VCardText>
        <VRow>
          <VCol cols="12" md="3">
            <VBtn block color="primary" variant="tonal" to="/admin/plans">
              <VIcon icon="tabler-plus" class="me-2" />
              Add New Plan
            </VBtn>
          </VCol>
          <VCol cols="12" md="3">
            <VBtn block color="success" variant="tonal" to="/admin/modules">
              <VIcon icon="tabler-plus" class="me-2" />
              Add New Module
            </VBtn>
          </VCol>
          <VCol cols="12" md="3">
            <VBtn block color="warning" variant="tonal">
              <VIcon icon="tabler-report" class="me-2" />
              Generate Report
            </VBtn>
          </VCol>
          <VCol cols="12" md="3">
            <VBtn block color="info" variant="tonal">
              <VIcon icon="tabler-settings" class="me-2" />
              System Settings
            </VBtn>
          </VCol>
        </VRow>
      </VCardText>
    </VCard>
  </div>
</template>
