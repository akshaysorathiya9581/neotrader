<script setup>
import { useSubscriptionStore } from '@/stores/subscription'

const store = useSubscriptionStore()

// Dialog states
const showPlanDialog = ref(false)
const editingPlan = ref(null)
const planForm = ref({
  name: '',
  price: 0,
  duration: 'month',
  description: '',
  features: [],
  moduleIds: [],
  color: 'primary',
  popular: false,
})

const featureInput = ref('')

const durationOptions = ['month', 'quarter', 'year']
const colorOptions = ['primary', 'success', 'info', 'warning', 'error']

// Open dialog for new plan
const openNewPlanDialog = () => {
  editingPlan.value = null
  planForm.value = {
    name: '',
    price: 0,
    duration: 'month',
    description: '',
    features: [],
    moduleIds: [],
    color: 'primary',
    popular: false,
  }
  showPlanDialog.value = true
}

// Open dialog for editing
const openEditDialog = (plan) => {
  editingPlan.value = plan
  planForm.value = { ...plan, features: [...plan.features], moduleIds: [...plan.moduleIds] }
  showPlanDialog.value = true
}

// Add feature
const addFeature = () => {
  if (featureInput.value.trim()) {
    planForm.value.features.push(featureInput.value.trim())
    featureInput.value = ''
  }
}

// Remove feature
const removeFeature = (index) => {
  planForm.value.features.splice(index, 1)
}

// Save plan
const savePlan = () => {
  if (editingPlan.value) {
    store.updatePlan(editingPlan.value.id, planForm.value)
  } else {
    store.addPlan(planForm.value)
  }
  showPlanDialog.value = false
}

// Delete plan
const deletePlan = (planId) => {
  if (confirm('Are you sure you want to delete this plan?')) {
    store.deletePlan(planId)
  }
}

// Get module names for plan
const getModuleNames = (moduleIds) => {
  return moduleIds.map(id => store.modules.find(m => m.id === id)?.name).filter(Boolean)
}
</script>

<template>
  <div>
    <!-- Header -->
    <VCard class="mb-4">
      <VCardText class="d-flex align-center justify-space-between flex-wrap gap-4 py-3">
        <div class="d-flex align-center gap-2">
          <VChip color="primary" variant="flat" size="small">Subscription Plans</VChip>
          <VIcon icon="tabler-home" size="18" />
          <span class="text-primary text-caption">Admin / Plans Management</span>
        </div>
        <VBtn color="primary" @click="openNewPlanDialog">
          <VIcon icon="tabler-plus" class="me-1" />
          Add New Plan
        </VBtn>
      </VCardText>
    </VCard>

    <!-- Plans Grid -->
    <VRow>
      <VCol v-for="plan in store.plans" :key="plan.id" cols="12" md="4">
        <VCard :class="plan.popular ? 'border-primary border-opacity-100' : ''">
          <VCardText class="text-center pa-6">
            <VChip v-if="plan.popular" color="primary" size="small" class="mb-2">Most Popular</VChip>
            <h4 class="text-h4 mb-2">{{ plan.name }}</h4>
            <p class="text-medium-emphasis mb-4">{{ plan.description }}</p>
            
            <div class="d-flex align-center justify-center mb-4">
              <span class="text-h3 font-weight-bold">₹{{ plan.price }}</span>
              <span class="text-medium-emphasis">/{{ plan.duration }}</span>
            </div>

            <VDivider class="mb-4" />

            <div class="text-left mb-4">
              <p class="text-body-2 font-weight-medium mb-2">Features:</p>
              <div v-for="(feature, idx) in plan.features" :key="idx" class="d-flex align-center gap-2 mb-1">
                <VIcon icon="tabler-check" size="16" color="success" />
                <span class="text-body-2">{{ feature }}</span>
              </div>
            </div>

            <VDivider class="mb-4" />

            <div class="text-left mb-4">
              <p class="text-body-2 font-weight-medium mb-2">Modules ({{ plan.moduleIds.length }}):</p>
              <div class="d-flex flex-wrap gap-1">
                <VChip v-for="name in getModuleNames(plan.moduleIds).slice(0, 5)" :key="name" size="x-small" color="info" variant="tonal">
                  {{ name }}
                </VChip>
                <VChip v-if="plan.moduleIds.length > 5" size="x-small" color="default">
                  +{{ plan.moduleIds.length - 5 }} more
                </VChip>
              </div>
            </div>

            <div class="d-flex gap-2 justify-center">
              <VBtn color="primary" variant="outlined" size="small" @click="openEditDialog(plan)">
                <VIcon icon="tabler-edit" size="16" class="me-1" />
                Edit
              </VBtn>
              <VBtn color="error" variant="outlined" size="small" @click="deletePlan(plan.id)">
                <VIcon icon="tabler-trash" size="16" class="me-1" />
                Delete
              </VBtn>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- Plan Dialog -->
    <VDialog v-model="showPlanDialog" max-width="700">
      <VCard>
        <VCardTitle class="d-flex justify-space-between align-center pa-4">
          <span>{{ editingPlan ? 'Edit Plan' : 'Add New Plan' }}</span>
          <VBtn icon variant="text" @click="showPlanDialog = false">
            <VIcon icon="tabler-x" />
          </VBtn>
        </VCardTitle>
        <VDivider />
        <VCardText class="pa-4">
          <VRow>
            <VCol cols="12" md="6">
              <VTextField v-model="planForm.name" label="Plan Name" placeholder="e.g., Professional" />
            </VCol>
            <VCol cols="12" md="3">
              <VTextField v-model.number="planForm.price" label="Price (₹)" type="number" />
            </VCol>
            <VCol cols="12" md="3">
              <VSelect v-model="planForm.duration" label="Duration" :items="durationOptions" />
            </VCol>
            <VCol cols="12">
              <VTextarea v-model="planForm.description" label="Description" rows="2" />
            </VCol>
            <VCol cols="12" md="6">
              <VSelect v-model="planForm.color" label="Color Theme" :items="colorOptions" />
            </VCol>
            <VCol cols="12" md="6">
              <VSwitch v-model="planForm.popular" label="Mark as Popular" color="primary" />
            </VCol>
            
            <!-- Features -->
            <VCol cols="12">
              <p class="text-body-2 font-weight-medium mb-2">Features</p>
              <div class="d-flex gap-2 mb-2">
                <VTextField v-model="featureInput" placeholder="Add a feature" density="compact" @keyup.enter="addFeature" />
                <VBtn color="primary" @click="addFeature">Add</VBtn>
              </div>
              <div class="d-flex flex-wrap gap-1">
                <VChip v-for="(feature, idx) in planForm.features" :key="idx" closable @click:close="removeFeature(idx)">
                  {{ feature }}
                </VChip>
              </div>
            </VCol>

            <!-- Modules -->
            <VCol cols="12">
              <p class="text-body-2 font-weight-medium mb-2">Select Modules</p>
              <div class="modules-grid">
                <VCheckbox
                  v-for="module in store.modules"
                  :key="module.id"
                  v-model="planForm.moduleIds"
                  :label="module.name"
                  :value="module.id"
                  density="compact"
                  hide-details
                />
              </div>
            </VCol>
          </VRow>
        </VCardText>
        <VDivider />
        <VCardActions class="pa-4">
          <VSpacer />
          <VBtn variant="outlined" @click="showPlanDialog = false">Cancel</VBtn>
          <VBtn color="primary" @click="savePlan">{{ editingPlan ? 'Update' : 'Create' }} Plan</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </div>
</template>

<style scoped>
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 8px;
}
</style>
