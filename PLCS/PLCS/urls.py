"""PLCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PLCS_system import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.login),
    path("register", views.register),
    path("login_user", views.login_user),
    path("register_user", views.register_user),
    path("dashboard", views.user_management),
    path("logout/", views.logout),
    path("disable_user/<int:user_id>/", views.disable_user),
    path("delete_user/<int:user_id>/", views.delete_user),

    #Project Management
    path("view_projects", views.view_projects),
    path("add_project", views.add_project),
    path("delete_project/<int:project_id_delete>/", views.delete_project),

    path("profile/", views.view_profile),
    path("messages/", views.view_messages),

    path("nm_user/", views.nm_user),

    
    path("roles_permissions/", views.roles_permissions),
    path("add_role/", views.add_role),
    path("delete_role/<int:role_id>/", views.delete_role),


    #User Management
    path("user_management/", views.user_management),
    path("update_user/<int:user_id>/", views.update_user),

    path("edit_permissions_for_role/<int:role_id>/", views.edit_permissions_for_role),
    path("admin_add_user/", views.admin_add_user),


    #Learning content
    path("learning_topic/", views.learning_topic),
    path("learning_content/<int:topic_id>/", views.learning_content),
    path("learning_content_modules/", views.learning_content_modules),


    path("add_module/", views.add_module),
    path("add_topic/<int:module_id>/", views.add_topic),
    path("view_topics/<int:module_id>/", views.view_topics),



    path("delete_module/<int:module_id>/", views.delete_module),
    path("edit_module/<int:module_id>/", views.edit_module),


    path("view_module/<int:module_id>/", views.view_module),

    path("like_project/", views.like_project),

    path("project_details/<int:project_id>/", views.project_details),

    path("apply_to_project/<int:project_id>/<int:project_poster_id>", views.apply_to_project),

    path("view_projects_collaborations/", views.view_projects_collaborations),
    path("profile_history/<int:user_id>/", views.profile_history),

    path("view_collab_requests/<int:project_id>/", views.view_collab_requests),
    path("accept_collab/<int:collab_id>/<int:requester_id>/<int:project_id>/", views.accept_collab),
    path("reject_collab/<int:collab_id>/", views.reject_collab),

    path("project_collab_tasks/<int:project_id>/", views.project_collab_tasks),
    path("add_summary_content/<int:topic_id>/", views.add_summary_content),
    path("delete_summary/<int:summary_id>/<int:module_id>/", views.delete_summary),


    #Bookmark projects
    path("bookmark/", views.bookmark),
    path("unbookmark/", views.unbookmark),
    path("get_saved_projects/", views.get_saved_projects),
]
