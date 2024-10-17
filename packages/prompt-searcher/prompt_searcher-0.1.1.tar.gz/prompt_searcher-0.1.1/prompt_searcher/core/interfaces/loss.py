class LossFunction:
    def score(self, y_pred, y_true) -> int:
        """
        Calculate the loss score between predicted and true values.

        Args:
            y_pred: The predicted values.
            y_true: The true values.

        Returns:
            int: The calculated loss score.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def winner(self, previous_loss, new_loss) -> bool:
        """
        Compare two loss scores and return the better one.
        Important to note that this method should return the score that is better,
        for example, if the loss function is MSE, then the score that is better is the one that is lower.
        If the loss function is accuracy, then the score that is better is the one that is higher.

        Args:
            previous_loss: The previous loss score.
            new_loss: The new loss score.

        Returns:
            int: The better score.
        """
        raise NotImplementedError("This method should be overridden by subclasses")
