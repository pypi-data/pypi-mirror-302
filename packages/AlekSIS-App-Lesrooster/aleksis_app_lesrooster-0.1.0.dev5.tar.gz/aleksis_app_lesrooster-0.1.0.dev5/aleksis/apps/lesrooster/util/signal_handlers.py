def create_time_grid_for_new_validity_range(sender, instance, created, **kwargs):
    from ..models import TimeGrid  # noqa

    if created:
        TimeGrid.objects.create(validity_range=instance)
