<script setup>
import { useSubscriptionStore } from '@/stores/subscription'

const store = useSubscriptionStore()

const currentPlan = computed(() => store.currentPlan)
const isYearly = ref(false)

// Calculate yearly price (20% discount)
const getPrice = (plan) => {
  if (isYearly.value) {
    return Math.round(plan.price * 12 * 0.8)
  }
  return plan.price
}

const getDuration = () => isYearly.value ? 'year' : 'month'

// Subscribe to plan
const subscribeToPlan = (planId) => {
  store.subscribeToPlan(planId)
  alert('Successfully subscribed! Your access has been updated.')
}

// Check if module is accessible
const isModuleAccessible = (moduleId) => {
  return store.accessibleModuleIds.includes(moduleId)
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
          <span class="text-primary text-caption">Choose Your Plan</span>
        </div>
        <div v-if="currentPlan" class="d-flex align-center gap-2">
          <span class="text-caption">Current Plan:</span>
          <VChip :color="currentPlan.color" size="small">{{ currentPlan.name }}</VChip>
        </div>
      </VCardText>
    </VCard>

    <!-- Billing Toggle -->
    <div class="text-center mb-6">
      <h2 class="text-h4 mb-2">Simple, Transparent Pricing</h2>
      <p class="text-medium-emphasis mb-4">Choose the plan that best fits your trading needs</p>
      
      <div class="d-flex align-center justify-center gap-3">
        <span :class="!isYearly ? 'font-weight-bold' : 'text-medium-emphasis'">Monthly</span>
        <VSwitch v-model="isYearly" hide-details color="primary" />
        <span :class="isYearly ? 'font-weight-bold' : 'text-medium-emphasis'">
          Yearly
          <VChip color="success" size="x-small" class="ms-1">Save 20%</VChip>
        </span>
      </div>
    </div>

    <!-- Plans Grid -->
    <VRow class="justify-center">
      <VCol v-for="plan in store.plans" :key="plan.id" cols="12" md="4">
        <VCard 
          :class="[
            plan.popular ? 'border-primary border-opacity-100 elevation-8' : '',
            currentPlan?.id === plan.id ? 'bg-light' : ''
          ]"
          class="plan-card"
        >
          <VCardText class="text-center pa-6">
            <!-- Popular Badge -->
            <div v-if="plan.popular" class="popular-badge">
              <VChip color="primary" size="small">Most Popular</VChip>
            </div>

            <!-- Current Plan Badge -->
            <VChip v-if="currentPlan?.id === plan.id" color="success" size="small" class="mb-2">
              <VIcon icon="tabler-check" size="14" class="me-1" />
              Current Plan
            </VChip>

            <h4 class="text-h4 mb-2">{{ plan.name }}</h4>
            <p class="text-medium-emphasis mb-4">{{ plan.description }}</p>
            
            <div class="d-flex align-center justify-center mb-4">
              <span class="text-h6 me-1">₹</span>
              <span class="text-h2 font-weight-bold">{{ getPrice(plan) }}</span>
              <span class="text-medium-emphasis">/{{ getDuration() }}</span>
            </div>

            <VBtn 
              :color="plan.popular ? 'primary' : 'default'"
              :variant="currentPlan?.id === plan.id ? 'outlined' : 'flat'"
              block
              size="large"
              class="mb-4"
              :disabled="currentPlan?.id === plan.id"
              @click="subscribeToPlan(plan.id)"
            >
              {{ currentPlan?.id === plan.id ? 'Current Plan' : 'Subscribe Now' }}
            </VBtn>

            <VDivider class="mb-4" />

            <!-- Features List -->
            <div class="text-left">
              <p class="text-body-2 font-weight-medium mb-3">What's included:</p>
              <div v-for="(feature, idx) in plan.features" :key="idx" class="d-flex align-center gap-2 mb-2">
                <VIcon icon="tabler-check" size="18" color="success" />
                <span class="text-body-2">{{ feature }}</span>
              </div>
            </div>

            <VDivider class="my-4" />

            <!-- Modules Count -->
            <div class="text-left">
              <p class="text-body-2 font-weight-medium mb-2">
                <VIcon icon="tabler-puzzle" size="16" class="me-1" />
                {{ plan.moduleIds.length }} Modules Included
              </p>
              <VExpansionPanels variant="accordion">
                <VExpansionPanel>
                  <VExpansionPanelTitle class="text-caption py-2">View all modules</VExpansionPanelTitle>
                  <VExpansionPanelText>
                    <div class="d-flex flex-wrap gap-1">
                      <VChip 
                        v-for="moduleId in plan.moduleIds" 
                        :key="moduleId" 
                        size="x-small"
                        :color="isModuleAccessible(moduleId) ? 'success' : 'default'"
                        variant="tonal"
                      >
                        {{ store.modules.find(m => m.id === moduleId)?.name }}
                      </VChip>
                    </div>
                  </VExpansionPanelText>
                </VExpansionPanel>
              </VExpansionPanels>
            </div>
          </VCardText>
        </VCard>
      </VCol>
    </VRow>

    <!-- FAQ Section -->
    <VCard class="mt-6">
      <VCardTitle class="py-3">Frequently Asked Questions</VCardTitle>
      <VCardText>
        <VExpansionPanels variant="accordion">
          <VExpansionPanel title="Can I upgrade my plan anytime?">
            <VExpansionPanelText>
              Yes! You can upgrade your plan at any time. The price difference will be prorated for the remaining period.
            </VExpansionPanelText>
          </VExpansionPanel>
          <VExpansionPanel title="What payment methods do you accept?">
            <VExpansionPanelText>
              We accept all major credit cards, debit cards, UPI, and net banking through our secure payment gateway.
            </VExpansionPanelText>
          </VExpansionPanel>
          <VExpansionPanel title="Is there a free trial?">
            <VExpansionPanelText>
              Yes, we offer a 7-day free trial for all new users. You can explore all features before committing to a plan.
            </VExpansionPanelText>
          </VExpansionPanel>
          <VExpansionPanel title="Can I cancel my subscription?">
            <VExpansionPanelText>
              You can cancel your subscription at any time. Your access will continue until the end of the billing period.
            </VExpansionPanelText>
          </VExpansionPanel>
        </VExpansionPanels>
      </VCardText>
    </VCard>
  </div>
</template>

<style scoped>
.plan-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.plan-card:hover {
  transform: translateY(-4px);
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
}

.bg-light {
  background-color: rgba(var(--v-theme-success), 0.05) !important;
}
</style>
