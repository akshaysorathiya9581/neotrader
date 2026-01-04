<script setup>
import { useSubscriptionStore } from '@/stores/subscription'

const store = useSubscriptionStore()

// Dialog states
const showModuleDialog = ref(false)
const editingModule = ref(null)
const moduleForm = ref({
  name: '',
  path: '',
  icon: 'tabler-apps',
  category: 'core',
})

const categoryOptions = ['core', 'technical', 'pivots', 'candlestick', 'alerts', 'advanced', 'trades']
const iconOptions = [
  'tabler-layout-dashboard', 'tabler-search', 'tabler-chart-line', 'tabler-trending-up',
  'tabler-chart-dots', 'tabler-activity', 'tabler-gauge', 'tabler-spiral',
  'tabler-arrows-split', 'tabler-chart-bar', 'tabler-chart-candle', 'tabler-chart-candle-filled',
  'tabler-bell-ringing', 'tabler-cloud', 'tabler-replace', 'tabler-clock', 'tabler-apps',
]

// Open dialog for new module
const openNewModuleDialog = () => {
  editingModule.value = null
  moduleForm.value = {
    name: '',
    path: '',
    icon: 'tabler-apps',
    category: 'core',
  }
  showModuleDialog.value = true
}

// Open dialog for editing
const openEditDialog = (module) => {
  editingModule.value = module
  moduleForm.value = { ...module }
  showModuleDialog.value = true
}

// Save module
const saveModule = () => {
  if (editingModule.value) {
    store.updateModule(editingModule.value.id, moduleForm.value)
  } else {
    store.addModule(moduleForm.value)
  }
  showModuleDialog.value = false
}

// Delete module
const deleteModule = (moduleId) => {
  if (confirm('Are you sure you want to delete this module? It will be removed from all plans.')) {
    store.deleteModule(moduleId)
  }
}

// Get plans that include this module
const getPlansForModule = (moduleId) => {
  return store.plans.filter(p => p.moduleIds.includes(moduleId)).map(p => p.name)
}

// Category label
const getCategoryLabel = (cat) => {
  const labels = {
    core: 'Core',
    technical: 'Technical Indicators',
    pivots: 'Pivot Analysis',
    candlestick: 'Candlestick',
    alerts: 'Alerts',
    advanced: 'Advanced',
    trades: 'Trades',
  }
  return labels[cat] || cat
}

const getCategoryColor = (cat) => {
  const colors = {
    core: 'primary',
    technical: 'success',
    pivots: 'info',
    candlestick: 'warning',
    alerts: 'error',
    advanced: 'secondary',
    trades: 'primary',
  }
  return colors[cat] || 'default'
}
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="success" variant="flat" size="small">Module Management</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-success text-caption">Admin / Modules Management</span>
        </div>
        <VBtn color="success" @click="openNewModuleDialog">
          <VIcon icon="tabler-plus" class="me-1" />
          Add New Module
        </VBtn>
      </VCardText>
    </VCard>

    <!-- Modules by Category -->
    <div v-for="(modules, category) in store.modulesByCategory" :key="category" class="mb-4">
      <h6 class="text-h6 mb-3 d-flex align-center gap-2">
        <VChip :color="getCategoryColor(category)" size="small">{{ getCategoryLabel(category) }}</VChip>
        <span class="text-medium-emphasis text-body-2">({{ modules.length }} modules)</span>
      </h6>
      
      <VRow>
        <VCol v-for="module in modules" :key="module.id" cols="12" md="4" lg="3">
          <VCard>
            <VCardText class="pa-4">
              <div class="d-flex align-center gap-3 mb-3">
                <VAvatar :color="getCategoryColor(category)" variant="tonal" size="42">
                  <VIcon :icon="module.icon" size="24" />
                </VAvatar>
                <div>
                  <h6 class="text-body-1 font-weight-medium">{{ module.name }}</h6>
                  <p class="text-caption text-medium-emphasis mb-0">{{ module.path }}</p>
                </div>
              </div>
              
              <div class="mb-3">
                <p class="text-caption text-medium-emphasis mb-1">Available in Plans:</p>
                <div class="d-flex flex-wrap gap-1">
                  <VChip v-for="plan in getPlansForModule(module.id)" :key="plan" size="x-small" color="info" variant="tonal">
                    {{ plan }}
                  </VChip>
                  <VChip v-if="getPlansForModule(module.id).length === 0" size="x-small" color="warning" variant="tonal">
                    No plans
                  </VChip>
                </div>
              </div>

              <div class="d-flex gap-2">
                <VBtn color="primary" variant="outlined" size="small" block @click="openEditDialog(module)">
                  <VIcon icon="tabler-edit" size="16" class="me-1" />
                  Edit
                </VBtn>
                <VBtn color="error" variant="outlined" size="small" icon @click="deleteModule(module.id)">
                  <VIcon icon="tabler-trash" size="16" />
                </VBtn>
              </div>
            </VCardText>
          </VCard>
        </VCol>
      </VRow>
    </div>

    <!-- Module Dialog -->
    <VDialog v-model="showModuleDialog" max-width="500">
      <VCard>
        <VCardTitle class="d-flex justify-space-between align-center pa-4">
          <span>{{ editingModule ? 'Edit Module' : 'Add New Module' }}</span>
          <VBtn icon variant="text" @click="showModuleDialog = false">
            <VIcon icon="tabler-x" />
          </VBtn>
        </VCardTitle>
        <VDivider />
        <VCardText class="pa-4">
          <VRow>
            <VCol cols="12">
              <VTextField v-model="moduleForm.name" label="Module Name" placeholder="e.g., ADX Trends" />
            </VCol>
            <VCol cols="12">
              <VTextField v-model="moduleForm.path" label="Route Path" placeholder="e.g., /technical/adx-trends" />
            </VCol>
            <VCol cols="12" md="6">
              <VSelect v-model="moduleForm.category" label="Category" :items="categoryOptions">
                <template #selection="{ item }">
                  {{ getCategoryLabel(item.value) }}
                </template>
                <template #item="{ item, props }">
                  <VListItem v-bind="props" :title="getCategoryLabel(item.value)" />
                </template>
              </VSelect>
            </VCol>
            <VCol cols="12" md="6">
              <VSelect v-model="moduleForm.icon" label="Icon" :items="iconOptions">
                <template #selection="{ item }">
                  <VIcon :icon="item.value" class="me-2" />
                  {{ item.value.replace('tabler-', '') }}
                </template>
                <template #item="{ item, props }">
                  <VListItem v-bind="props">
                    <template #prepend>
                      <VIcon :icon="item.value" class="me-2" />
                    </template>
                    <VListItemTitle>{{ item.value.replace('tabler-', '') }}</VListItemTitle>
                  </VListItem>
                </template>
              </VSelect>
            </VCol>
            <VCol cols="12">
              <div class="d-flex align-center gap-3 pa-3 bg-light rounded">
                <VAvatar :color="getCategoryColor(moduleForm.category)" variant="tonal" size="48">
                  <VIcon :icon="moduleForm.icon" size="28" />
                </VAvatar>
                <div>
                  <h6 class="text-body-1 font-weight-medium">{{ moduleForm.name || 'Module Preview' }}</h6>
                  <p class="text-caption text-medium-emphasis mb-0">{{ moduleForm.path || '/path/to/module' }}</p>
                </div>
              </div>
            </VCol>
          </VRow>
        </VCardText>
        <VDivider />
        <VCardActions class="pa-4">
          <VSpacer />
          <VBtn variant="outlined" @click="showModuleDialog = false">Cancel</VBtn>
          <VBtn color="success" @click="saveModule">{{ editingModule ? 'Update' : 'Create' }} Module</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </div>
</template>

<style scoped>
.bg-light {
  background-color: rgba(var(--v-theme-on-surface), 0.04);
}
</style>
