from django.contrib import admin
from .models import Carousel, Proposal, Category, Locality, Inscription, Phase, Settings, Testimony, Tool, Partner, SocialMedia

class ProposalAdmin(admin.ModelAdmin): 
    list_display = ['name', 'group_name', 'contact_name', 'approved']
    search_fields = ['name', 'group_name', 'contact_name']
    list_filter = ('approved', 'category', 'locality')
    readonly_fields = ('created', 'terms_service')

class CategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']
    search_fields = ['name']

class LocalityAdmin(admin.ModelAdmin): 
    list_display = ['name']
    search_fields = ['name']

class PhaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'number']
    search_fields = ['title']

class InscriptionAdmin(admin.ModelAdmin): 
    list_display = ['name', 'begins', 'ends', 'state']
    search_fields = ['name']
    readonly_fields = ('created', 'state')

class ToolAdmin(admin.ModelAdmin): 
    list_display = ['name', 'description']

class TestimonyAdmin(admin.ModelAdmin): 
    list_display = ['name', 'created']
    search_fields = ['name']
    readonly_fields = ('created', )

class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['name', 'number']

admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(Phase, PhaseAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(Testimony, TestimonyAdmin)
admin.site.register(Carousel)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)


class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Settings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Settings, SettingsAdmin)