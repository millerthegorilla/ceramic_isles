# django_forum

my django site set up for ceramic isles

I am developing the django project structure to allow me to easily set up new sites with the minimum of fuss.

django_users_app is a django app that adds email field to the basic user functionality, as well as having a fleshed out and styled set of templates.  It includes django-email-verification to send an email to new users.

django_profile is a django app that has a simple profile that includes a display name field and has a template for updating the profile.

django_posts_and_comments is a django app that has a framework for storing and displaying posts and associated comments.  I build on that functionality in django_forum_app, but it could easily be used in a blogging application or similar.

django_forum_app is a forum that incorporates django_posts_and_comments and django_profile, and has forum rules, as well as adding moderation to the posts and comments.

django_artisan is a complete site that is the reason I started djangoing, and offers the opportunity to easily customise and launch a web site that offers a forum for artisans in some area, and that also displays the artisan's work on the landing page, as well as on their own personal page.

All code is released under the GPL v3.0 license a copy of which is included in this repository.
