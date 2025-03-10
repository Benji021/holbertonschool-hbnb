#!/usr/bin/python3
""" Defining the review class, its attributes and relationships """


from datetime import datetime

class Review:
    def __init__(self, text, rating, place, user, review_id=None):
        """
        Initializes a new review.
        :param review_id: Unique review identifier
        :param text: Review content (mandatory)
        :param rating: Rating given (between 1 and 5)
        :param place: Instance of place under review
        :param user: Instance of the user who wrote the review
        """
        if not (1 <= rating <= 5):
            raise ValueError("The score must be between 1 and 5")

        self.review_id = review_id
        self.text = text
        self.rating = rating # Score between 1 and 5
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        # Relation
        self.user = user # User who wrote the review
        self.place = place # The place concerned by the review

        if user:
            user.add_review(self) # Add review to user


    def __str__(self):
        """ Returns a textual representation of the review """
        return f"Review by {self.user}: {self.rating}/5 - {self.text} ({self.created_at})"

    def updated_review(self, text=None, rating=None):
        """ Updates review rating or comment """
        if rating is not None:
            if not (1 <= rating <= 5):
                raise ValueError("The score must be between 1 and 5")
        self.rating = rating

        if text is not None:
            self.text = text

        self.updated_at = datetime.now()