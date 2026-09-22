from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError

from shortener.domain.errors import DuplicatedCodeError
from shortener.domain.models import Link

CONDITIONAL_CHECK_FAILED = "ConditionalCheckFailedException"


class DynamoDbLinkRepository:
    def __init__(self, table: Any) -> None:
        self._table = table

    async def add(self, link: Link) -> None:
        try:
            await self._table.put_item(
                Item={
                    "code": link.code,
                    "target_url": link.target_url,
                    "created_at": link.created_at.isoformat(),
                    "visits": link.visits,
                },
                ConditionExpression="attribute_not_exists(code)",
            )
        except ClientError as error:
            if self._is_conditional_check_failure(error):
                raise DuplicatedCodeError(link.code) from error
            raise

    async def get(self, code: str) -> Link | None:
        response = await self._table.get_item(Key={"code": code})
        item = response.get("Item")
        return self._to_domain(item) if item is not None else None

    async def register_visit(self, code: str) -> Link | None:
        try:
            response = await self._table.update_item(
                Key={"code": code},
                UpdateExpression="SET visits = visits + :increment",
                ConditionExpression="attribute_exists(code)",
                ExpressionAttributeValues={":increment": 1},
                ReturnValues="ALL_NEW",
            )
        except ClientError as error:
            if self._is_conditional_check_failure(error):
                return None
            raise
        return self._to_domain(response["Attributes"])

    @staticmethod
    def _is_conditional_check_failure(error: ClientError) -> bool:
        return error.response["Error"]["Code"] == CONDITIONAL_CHECK_FAILED

    @staticmethod
    def _to_domain(item: dict[str, Any]) -> Link:
        return Link(
            code=item["code"],
            target_url=item["target_url"],
            created_at=datetime.fromisoformat(item["created_at"]),
            visits=int(item["visits"]),
        )
