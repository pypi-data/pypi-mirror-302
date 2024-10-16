from typing import Any, Literal, Union

import pandas as pd
from pydantic import BaseModel
from scipy.stats import ttest_ind

from abtestools.audiences import Audience, User


class Metric(BaseModel):
    """
    Test metric
    """

    name: str
    type: Literal["discrete", "continuous"]


class TestResult(BaseModel):
    """
    # TestResult
    Results of a statistical test

    ### Parameters
        - total_test_metric: float
        - total_control_metric: float
        - test_metric_per_user: float
        - control_metric_per_user: float
        - relative_uplift: float
        - absolute_uplift: float
        - metric_driven_by_test: float
    """

    total_test_metric: float
    total_control_metric: float
    test_metric_per_user: float
    control_metric_per_user: float
    relative_uplift: float
    absolute_uplift: float
    metric_driven_by_test: float


class Test:
    """
    # Test
    ### Description
    Statistical AB test, that will provide tools to calculate statistical significance, uplift and other useful metrics

    ### Parameters
        - audience: <a style="color:#FF0000">Audience</a> object containing the users involved in the test
        - metric: Specify if the metric is discrete (1 or 0 values per user) or continuous.
        - data: dictionary containing the identifiers of the user as key and the value of the metric as value. If instead
            of using the original identifier you use the audience uuid, use the **use_uuid** parameter in the methods of
            this class.

    ### Methods
    - significance: Returns a touple with the p-value, the statistic and the confidence interval
    - invert_audience_groups: Inverts test and holdout groups on the audience
    - test_results: returns a 'TestResult' object
    """

    def __init__(
        self,
        audience: Audience,
        metric: Literal["discrete", "continuous"],
        data: dict[Any, Union[int, float]],
    ):
        self.audience = audience
        self.metric = metric
        self.data = data

    def significance(self, use_uuid: bool = False) -> tuple[float, float, Any]:
        """
        Calculate the Statistical Significance of the Test.
        -----------------
        ### Parameters:
        - use_uuid: Boolean to use the uuid as user reference. If False, the user identifier will be used instead

        ### Outputs
        - Tuple (
            - p value: p value of the test
            - statistic: statistical result of the test
            - confidence interval
        )
        """
        test = list(filter(lambda x: x.group == "test", self.audience.users))
        control = list(filter(lambda x: x.group == "control", self.audience.users))

        identifier = "uuid" if use_uuid else "identifier"

        test_data = pd.DataFrame({"user_id": [*test]})
        test_data["group"] = "test"
        test_data["user_id"] = (
            test_data["user_id"].apply(lambda x: getattr(x, identifier)).astype(str)
        )
        test_data["metric"] = test_data["user_id"].map(self.data)
        control_data = pd.DataFrame({"user_id": [*control]})
        control_data["group"] = "control"
        control_data["user_id"] = (
            control_data["user_id"].apply(lambda x: getattr(x, identifier)).astype(str)
        )
        control_data["metric"] = control_data["user_id"].map(self.data)

        result = ttest_ind(a=test_data["metric"].to_list(), b=control_data["metric"].to_list())
        return (
            float(result.pvalue),
            float(result.statistic),
            result.confidence_interval,
        )

    def invert_audience_groups(self) -> "Test":
        self.audience.invert_groups()

    def test_results(self, use_uuid: bool = False) -> Any:
        test = list(filter(lambda x: x.group == "test", self.audience.users))
        control = list(filter(lambda x: x.group == "control", self.audience.users))
        identifier = "uuid" if use_uuid else "identifier"
        if not isinstance(list(self.data.keys())[0], str):
            self.data = {str(k): v for k, v in self.data.items()}

        test_data = pd.DataFrame({"user_id": [*test]})
        test_data["group"] = "test"
        test_data["user_id"] = (
            test_data["user_id"].apply(lambda x: getattr(x, identifier)).astype(str)
        )
        test_data["metric"] = test_data["user_id"].map(self.data)
        control_data = pd.DataFrame({"user_id": [*control]})
        control_data["group"] = "control"
        control_data["user_id"] = (
            control_data["user_id"].apply(lambda x: getattr(x, identifier)).astype(str)
        )
        control_data["metric"] = control_data["user_id"].map(self.data)
        df = pd.concat([test_data, control_data])

        test_users = len(df.loc[df.group == "test"])
        control_users = len(df.loc[df.group == "control"])

        test_metric = df.loc[df.group == "test", "metric"].sum()
        control_metric = df.loc[df.group == "control", "metric"].sum()

        test_metric_per_user = test_metric / test_users
        control_metric_per_user = control_metric / control_users

        relative_uplift = (test_metric_per_user / control_metric_per_user) - 1
        absolute_uplift = test_metric - control_metric

        metric_by_test = test_metric - (test_metric / relative_uplift)

        return TestResult(
            total_test_metric=test_metric,
            total_control_metric=control_metric,
            test_metric_per_user=test_metric_per_user,
            control_metric_per_user=control_metric_per_user,
            relative_uplift=relative_uplift,
            absolute_uplift=absolute_uplift,
            metric_driven_by_test=metric_by_test,
        )
